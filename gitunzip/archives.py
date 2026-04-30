"""Archive extraction with support for multiple formats."""

import os
import re
import shutil
import logging
import zipfile
import tarfile
from pathlib import Path
from typing import List, Optional, Tuple

logger = logging.getLogger(__name__)

SUPPORTED_EXTENSIONS = (".zip", ".tar.gz", ".tgz", ".7z", ".rar", ".bz2", ".xz")

# Patterns to exclude from extraction (junk files)
DEFAULT_EXCLUDE_PATTERNS = [
    "__pycache__", "*.pyc", "*.pyo", ".git", "node_modules",
    ".DS_Store", "Thumbs.db", "*.swp", "*.swo", ".env",
    ".env.local", "*.log", ".pytest_cache", ".mypy_cache",
]


def is_archive(filename: str) -> bool:
    """Check if a file is a supported archive."""
    lower = filename.lower()
    return any(lower.endswith(ext) for ext in SUPPORTED_EXTENSIONS)


def get_archive_format(filename: str) -> str:
    """Detect archive format from filename."""
    lower = filename.lower()
    if lower.endswith(".zip"):
        return "zip"
    elif lower.endswith((".tar.gz", ".tgz")):
        return "tar.gz"
    elif lower.endswith(".bz2"):
        return "bz2"
    elif lower.endswith(".xz"):
        return "xz"
    elif lower.endswith(".7z"):
        return "7z"
    elif lower.endswith(".rar"):
        return "rar"
    return "unknown"


def should_exclude(path: str, exclude_patterns: List[str]) -> bool:
    """Check if a path should be excluded based on patterns."""
    parts = Path(path).parts
    for pattern in exclude_patterns:
        # Check each part of the path
        for part in parts:
            if _match_pattern(part, pattern):
                return True
        # Also check the full filename
        if _match_pattern(Path(path).name, pattern):
            return True
    return False


def _match_pattern(text: str, pattern: str) -> bool:
    """Simple glob-style pattern matching."""
    import fnmatch
    return fnmatch.fnmatch(text, pattern)


def extract_zip(filepath: str, extract_dir: str, exclude_patterns: List[str] = None) -> Tuple[List[str], List[str]]:
    """Extract a ZIP archive. Returns (extracted_files, skipped_files)."""
    exclude_patterns = exclude_patterns or DEFAULT_EXCLUDE_PATTERNS
    extracted = []
    skipped = []

    # Validate ZIP integrity first
    if not zipfile.is_zipfile(filepath):
        raise ValueError(f"Invalid or corrupted ZIP file: {filepath}")

    with zipfile.ZipFile(filepath, "r") as zf:
        # Check for zip bombs (uncompressed > 1GB)
        total_uncompressed = sum(info.file_size for info in zf.infolist())
        if total_uncompressed > 1024 * 1024 * 1024:
            raise ValueError(f"Archive too large when uncompressed ({total_uncompressed / 1024 / 1024:.0f} MB). Possible zip bomb.")

        for info in zf.infolist():
            if should_exclude(info.filename, exclude_patterns):
                skipped.append(info.filename)
                continue
            # Path traversal check
            target = os.path.join(extract_dir, info.filename)
            real_target = os.path.realpath(target)
            if not real_target.startswith(os.path.realpath(extract_dir)):
                logger.warning("Blocked path traversal attempt: %s", info.filename)
                skipped.append(info.filename)
                continue
            zf.extract(info, extract_dir)
            extracted.append(info.filename)

    return extracted, skipped


def extract_tar(filepath: str, extract_dir: str, exclude_patterns: List[str] = None) -> Tuple[List[str], List[str]]:
    """Extract a tar.gz/tgz/bz2/xz archive."""
    exclude_patterns = exclude_patterns or DEFAULT_EXCLUDE_PATTERNS
    extracted = []
    skipped = []

    if not tarfile.is_tarfile(filepath):
        raise ValueError(f"Invalid or corrupted tar file: {filepath}")

    with tarfile.open(filepath, "r:*") as tf:
        for member in tf.getmembers():
            if should_exclude(member.name, exclude_patterns):
                skipped.append(member.name)
                continue
            # Path traversal check
            target = os.path.join(extract_dir, member.name)
            real_target = os.path.realpath(target)
            if not real_target.startswith(os.path.realpath(extract_dir)):
                logger.warning("Blocked path traversal attempt: %s", member.name)
                skipped.append(member.name)
                continue
            # Skip symlinks if configured
            if member.issym() or member.islnk():
                skipped.append(member.name)
                continue
            tf.extract(member, extract_dir, filter="data")
            extracted.append(member.name)

    return extracted, skipped


def extract_7z(filepath: str, extract_dir: str, exclude_patterns: List[str] = None) -> Tuple[List[str], List[str]]:
    """Extract a 7z archive."""
    try:
        import py7zr
    except ImportError:
        raise ImportError("py7zr is required for .7z support. Install with: pip install py7zr")

    exclude_patterns = exclude_patterns or DEFAULT_EXCLUDE_PATTERNS
    extracted = []
    skipped = []

    with py7zr.SevenZipFile(filepath, "r") as sz:
        all_files = sz.getnames()
        for name in all_files:
            if should_exclude(name, exclude_patterns):
                skipped.append(name)
                continue
            extracted.append(name)

        # Extract only non-excluded files
        if extracted:
            sz.extractall(extract_dir)

    return extracted, skipped


def extract_rar(filepath: str, extract_dir: str, exclude_patterns: List[str] = None) -> Tuple[List[str], List[str]]:
    """Extract a RAR archive."""
    try:
        import rarfile
    except ImportError:
        raise ImportError("rarfile is required for .rar support. Install with: pip install rarfile")

    exclude_patterns = exclude_patterns or DEFAULT_EXCLUDE_PATTERNS
    extracted = []
    skipped = []

    with rarfile.RarFile(filepath, "r") as rf:
        for info in rf.infolist():
            if should_exclude(info.filename, exclude_patterns):
                skipped.append(info.filename)
                continue
            rf.extract(info, extract_dir)
            extracted.append(info.filename)

    return extracted, skipped


def extract_archive(filepath: str, extract_dir: str, exclude_patterns: List[str] = None) -> Tuple[List[str], List[str]]:
    """Extract any supported archive. Returns (extracted_files, skipped_files)."""
    fmt = get_archive_format(filepath)

    extractors = {
        "zip": extract_zip,
        "tar.gz": extract_tar,
        "bz2": extract_tar,
        "xz": extract_tar,
        "7z": extract_7z,
        "rar": extract_rar,
    }

    extractor = extractors.get(fmt)
    if not extractor:
        raise ValueError(f"Unsupported archive format: {filepath}")

    logger.info("Extracting %s (%s format)", filepath, fmt)
    return extractor(filepath, extract_dir, exclude_patterns)


def get_archive_info(filepath: str) -> dict:
    """Get archive metadata without extracting."""
    size_bytes = os.path.getsize(filepath)
    fmt = get_archive_format(filepath)
    info = {
        "filename": os.path.basename(filepath),
        "format": fmt,
        "size_bytes": size_bytes,
        "size_mb": round(size_bytes / (1024 * 1024), 2),
        "file_count": 0,
    }

    try:
        if fmt == "zip" and zipfile.is_zipfile(filepath):
            with zipfile.ZipFile(filepath, "r") as zf:
                info["file_count"] = len(zf.infolist())
                info["compressed_size"] = sum(i.compress_size for i in zf.infolist())
                info["uncompressed_size"] = sum(i.file_size for i in zf.infolist())
        elif fmt in ("tar.gz", "bz2", "xz") and tarfile.is_tarfile(filepath):
            with tarfile.open(filepath, "r:*") as tf:
                info["file_count"] = len(tf.getmembers())
        elif fmt == "7z":
            try:
                import py7zr
                with py7zr.SevenZipFile(filepath, "r") as sz:
                    info["file_count"] = len(sz.getnames())
            except ImportError:
                pass
    except Exception as e:
        logger.warning("Could not read archive info: %s", e)

    return info
