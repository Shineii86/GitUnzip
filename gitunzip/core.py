"""Core processing logic for GitUnzip."""

import os
import shutil
import tempfile
import logging
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field

from .archives import extract_archive, get_archive_info, is_archive, DEFAULT_EXCLUDE_PATTERNS
from .github_ops import (
    ensure_repo_exists, clone_repo, create_branch, copy_files,
    commit_and_push, get_repo_url, generate_merge_pr_url,
    DEFAULT_COMMIT_MSG, TOOL_WATERMARK,
)
from .notifications import EmailNotifier, TelegramNotifier
from .qrcodes import generate_qr
from .config import AppConfig

logger = logging.getLogger(__name__)


@dataclass
class ArchiveResult:
    """Result of processing a single archive."""
    filename: str
    success: bool
    file_count: int = 0
    extracted_count: int = 0
    skipped_count: int = 0
    size_mb: float = 0
    error: Optional[str] = None
    duration_seconds: float = 0


@dataclass
class UploadResult:
    """Result of the entire upload operation."""
    success: bool
    repo_url: str = ""
    branch: str = ""
    archives: List[ArchiveResult] = field(default_factory=list)
    total_files: int = 0
    total_skipped: int = 0
    duration_seconds: float = 0
    error: Optional[str] = None


def process_archive_file(
    filename: str,
    file_data: bytes,
    temp_dir: str,
    target_path: Path,
    exclude_patterns: List[str],
) -> ArchiveResult:
    """Process a single archive file: extract and copy to target."""
    start_time = time.time()
    result = ArchiveResult(filename=filename, success=False, size_mb=len(file_data) / (1024 * 1024))

    try:
        # Get archive info
        info = get_archive_info(filename)
        result.file_count = info.get("file_count", 0)

        # Write to temp file
        temp_file = os.path.join(temp_dir, filename)
        with open(temp_file, "wb") as f:
            f.write(file_data)

        # Extract
        extract_dir = os.path.join(temp_dir, f"extract_{Path(filename).stem}")
        os.makedirs(extract_dir, exist_ok=True)

        extracted, skipped = extract_archive(temp_file, extract_dir, exclude_patterns)
        result.extracted_count = len(extracted)
        result.skipped_count = len(skipped)

        if not extracted:
            result.error = "No files extracted (all excluded or empty archive)"
            return result

        # Copy to target
        copied = copy_files(extract_dir, str(target_path), exclude_patterns)
        logger.info("Copied %d files from %s", copied, filename)

        result.success = True
        result.duration_seconds = time.time() - start_time
        return result

    except Exception as e:
        result.error = str(e)
        result.duration_seconds = time.time() - start_time
        logger.error("Failed to process %s: %s", filename, e)
        return result


def process_uploads(config: AppConfig, uploaded_files: Optional[Dict[str, bytes]] = None) -> UploadResult:
    """
    Main processing function.
    If uploaded_files is None, will prompt for file upload (Colab mode).
    """
    start_time = time.time()
    gh = config.github
    result = UploadResult(success=False, branch=gh.branch)

    # Setup notifications
    email_notifier = EmailNotifier(
        enabled=config.email.enabled,
        sender=config.email.sender,
        to=config.email.to,
        password=config.email.password,
        smtp_server=config.email.smtp_server,
        smtp_port=config.email.smtp_port,
    )
    telegram_notifier = TelegramNotifier(
        bot_token=config.telegram.bot_token,
        chat_id=config.telegram.chat_id,
    )

    # Get files to process
    if uploaded_files is None:
        try:
            from google.colab import files as colab_files
            print("\n📤 Please select your archive file(s)...")
            print("   Supported: .zip, .tar.gz, .tgz, .7z, .rar, .bz2, .xz")
            print("   (Tap 'Choose Files' — you can select multiple)")
            uploaded_files = colab_files.upload()
        except ImportError:
            logger.error("No files provided and not running in Colab.")
            result.error = "No files provided"
            return result

    if not uploaded_files:
        result.error = "No files uploaded"
        return result

    # Filter archives
    archive_files = {f: d for f, d in uploaded_files.items() if is_archive(f)}
    if not archive_files:
        result.error = "No supported archive files found"
        return result

    print(f"\n✅ Found {len(archive_files)} archive(s) to process")

    # Show archive info
    for filename in archive_files:
        info = get_archive_info(filename) if os.path.exists(filename) else {"size_mb": len(archive_files[filename]) / (1024*1024)}
        print(f"   📦 {filename} ({info.get('size_mb', 0):.2f} MB, ~{info.get('file_count', '?')} files)")

    # Ensure repo exists
    try:
        ensure_repo_exists(gh.username, gh.token, gh.repo_name, gh.private_repo)
    except RuntimeError as e:
        result.error = str(e)
        return result

    # Clone repo
    temp_base = tempfile.mkdtemp()
    repo_dir = tempfile.mkdtemp()

    try:
        print(f"\n📥 Cloning repository '{gh.repo_name}'...")
        repo = clone_repo(gh.username, gh.token, gh.repo_name, gh.branch, repo_dir)
        print("✅ Repository cloned")
    except RuntimeError as e:
        result.error = str(e)
        _cleanup(temp_base, repo_dir)
        return result

    # Branch handling
    actual_branch = gh.branch
    if not gh.overwrite_branch:
        try:
            actual_branch = create_branch(repo, gh.branch)
            result.branch = actual_branch
            print(f"\n🌿 Created new branch: {actual_branch}")
        except RuntimeError as e:
            result.error = str(e)
            _cleanup(temp_base, repo_dir)
            return result

    # Target path
    target_path = Path(repo_dir)
    if gh.target_subdir:
        target_path = target_path / gh.target_subdir
        target_path.mkdir(parents=True, exist_ok=True)

    # Process archives
    exclude_patterns = config.extract.exclude_patterns
    for filename, data in archive_files.items():
        archive_result = process_archive_file(
            filename, data, temp_base, target_path, exclude_patterns,
        )
        result.archives.append(archive_result)
        result.total_files += archive_result.extracted_count
        result.total_skipped += archive_result.skipped_count

        if archive_result.success:
            print(f"   ✅ {filename}: {archive_result.extracted_count} files extracted")
        else:
            print(f"   ❌ {filename}: {archive_result.error}")

    successful = [a for a in result.archives if a.success]
    if not successful:
        result.error = "No archives were successfully processed"
        _cleanup(temp_base, repo_dir)
        return result

    # Commit message
    commit_msg = gh.custom_commit_msg or DEFAULT_COMMIT_MSG

    # Commit and push
    try:
        print(f"\n💾 Committing changes...")
        pushed = commit_and_push(
            repo, commit_msg, actual_branch,
            force_push=gh.overwrite_branch,
            username=gh.username,
            email=f"{gh.username}@users.noreply.github.com",
        )
        if pushed:
            print(f"✅ Push successful to branch '{actual_branch}'!")
        else:
            print("ℹ️ No changes to commit")
    except RuntimeError as e:
        result.error = str(e)
        _cleanup(temp_base, repo_dir)
        return result

    # Cleanup
    _cleanup(temp_base, repo_dir)

    # Results
    result.success = True
    result.repo_url = get_repo_url(gh.username, gh.repo_name, actual_branch)
    result.duration_seconds = time.time() - start_time

    # Generate QR
    print("\n" + "=" * 50)
    print("✨ Success! Your code is on GitHub.")
    print(f"📱 Scan QR code to open on another device:\n")
    try:
        qr_path = generate_qr(result.repo_url)
        from IPython.display import display, Image
        display(Image(qr_path))
    except Exception:
        pass
    print(f"🔗 {result.repo_url}")

    # PR link if new branch
    if not gh.overwrite_branch:
        pr_url = generate_merge_pr_url(gh.username, gh.repo_name, actual_branch, gh.branch)
        print(f"\n🔀 Create a PR to merge: {pr_url}")

    # Summary
    print(f"\n📊 Summary:")
    print(f"   Archives processed: {len(successful)}/{len(archive_files)}")
    print(f"   Total files: {result.total_files}")
    if result.total_skipped:
        print(f"   Files skipped: {result.total_skipped}")
    print(f"   Duration: {result.duration_seconds:.1f}s")
    print(f"   Branch: {actual_branch}")

    # Notifications
    notif_body = (
        f"✅ GitUnzip Upload Complete\n"
        f"Repo: {gh.username}/{gh.repo_name}\n"
        f"Branch: {actual_branch}\n"
        f"Files: {result.total_files}\n"
        f"Archives: {len(successful)}\n"
        f"URL: {result.repo_url}"
    )

    if email_notifier.send(f"✅ GitUnzip: {gh.repo_name}", notif_body):
        print("📧 Email notification sent!")
    if telegram_notifier.send(notif_body):
        print("📲 Telegram notification sent!")

    print(f"\n---")
    print(f"📱 Powered by [{TOOL_WATERMARK}]")

    return result


def _cleanup(*dirs):
    """Remove temporary directories."""
    for d in dirs:
        try:
            shutil.rmtree(d, ignore_errors=True)
        except Exception:
            pass
