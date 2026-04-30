"""GitHub repository operations."""

import os
import time
import shutil
import logging
from pathlib import Path
from typing import Optional, List

import requests
from git import Repo, GitCommandError

logger = logging.getLogger(__name__)

TOOL_WATERMARK = "Shineii86/GitUnzip"
DEFAULT_COMMIT_MSG = f"📤 Uploaded By [{TOOL_WATERMARK}]"


def ensure_repo_exists(username: str, token: str, repo_name: str, private: bool = False) -> bool:
    """Check if repo exists; create it if not."""
    url = f"https://api.github.com/repos/{username}/{repo_name}"
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"}

    resp = requests.get(url, headers=headers, timeout=15)
    if resp.status_code == 200:
        logger.info("Repository '%s' exists.", repo_name)
        return True

    if resp.status_code == 404:
        logger.info("Creating %s repo '%s'...", "private" if private else "public", repo_name)
        create_data = {"name": repo_name, "private": private, "auto_init": True}
        create_resp = requests.post(
            "https://api.github.com/user/repos",
            headers=headers, json=create_data, timeout=15,
        )
        if create_resp.status_code == 201:
            logger.info("Repository created successfully.")
            time.sleep(3)
            return True
        raise RuntimeError(f"Failed to create repo: {create_resp.text}")

    raise RuntimeError(f"GitHub API error: {resp.status_code} {resp.text}")


def clone_repo(username: str, token: str, repo_name: str, branch: str, target_dir: str) -> Repo:
    """Clone a repository to a local directory."""
    repo_url = f"https://{username}:{token}@github.com/{username}/{repo_name}.git"
    try:
        repo = Repo.clone_from(repo_url, target_dir, branch=branch)
        logger.info("Repository cloned to %s", target_dir)
        return repo
    except GitCommandError as e:
        raise RuntimeError(f"Clone failed: {e}")


def create_branch(repo: Repo, base_branch: str, new_branch_name: Optional[str] = None) -> str:
    """Create a new branch. Returns the branch name."""
    if new_branch_name is None:
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        new_branch_name = f"{base_branch}-upload-{timestamp}"

    try:
        repo.git.checkout("-b", new_branch_name)
        logger.info("Created branch: %s", new_branch_name)
        return new_branch_name
    except GitCommandError as e:
        raise RuntimeError(f"Failed to create branch: {e}")


def copy_files(source_dir: str, target_dir: str, exclude_patterns: List[str] = None) -> int:
    """Copy files from source to target. Returns count of files copied."""
    from .archives import should_exclude

    exclude_patterns = exclude_patterns or []
    source = Path(source_dir)
    target = Path(target_dir)
    count = 0

    for item in source.rglob("*"):
        if item.is_file():
            rel_path = item.relative_to(source)
            rel_str = str(rel_path)

            if should_exclude(rel_str, exclude_patterns):
                continue

            dest = target / rel_path
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, dest)
            count += 1

    return count


def commit_and_push(repo: Repo, commit_message: str, branch: str, force_push: bool = True,
                    username: str = "", email: str = "") -> bool:
    """Commit all changes and push to remote."""
    # Configure git user
    if username:
        repo.config_writer().set_value("user", "name", username).release()
    if email:
        repo.config_writer().set_value("user", "email", email).release()

    # Stage all changes
    repo.git.add(A=True)

    # Check if there are changes
    if not repo.index.diff("HEAD") and not repo.untracked_files:
        logger.info("No changes to commit.")
        return False

    # Commit
    repo.index.commit(commit_message)
    logger.info("Committed: '%s'", commit_message)

    # Push
    try:
        origin = repo.remote(name="origin")
        origin.push(branch, force=force_push)
        logger.info("Push successful to branch '%s'.", branch)
        return True
    except GitCommandError as e:
        raise RuntimeError(f"Push failed: {e}")


def get_repo_url(username: str, repo_name: str, branch: str = "main") -> str:
    """Get the GitHub repo URL."""
    return f"https://github.com/{username}/{repo_name}/tree/{branch}"


def generate_merge_pr_url(username: str, repo_name: str, source_branch: str, target_branch: str = "main") -> str:
    """Generate a URL to create a merge PR."""
    return f"https://github.com/{username}/{repo_name}/compare/{target_branch}...{source_branch}?expand=1"
