"""Configuration management for GitUnzip."""

import os
import json
from dataclasses import dataclass, field, asdict


@dataclass
class GitHubConfig:
    username: str = ""
    token: str = ""
    repo_name: str = "my-uploaded-code"
    branch: str = "main"
    overwrite_branch: bool = True
    target_subdir: str = ""
    private_repo: bool = False
    custom_commit_msg: str = ""


@dataclass
class EmailConfig:
    enabled: bool = False
    to: str = ""
    sender: str = ""
    password: str = ""
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 465


@dataclass
class TelegramConfig:
    bot_token: str = ""
    chat_id: str = ""


@dataclass
class ExtractOptions:
    """Options for archive extraction."""
    exclude_patterns: list = field(default_factory=lambda: [
        "__pycache__", "*.pyc", ".git", "node_modules",
        ".DS_Store", "Thumbs.db", "*.swp", ".env",
    ])
    max_file_size_mb: int = 500  # Max total extraction size
    follow_symlinks: bool = False


@dataclass
class AppConfig:
    """Root configuration for GitUnzip."""
    github: GitHubConfig = field(default_factory=GitHubConfig)
    email: EmailConfig = field(default_factory=EmailConfig)
    telegram: TelegramConfig = field(default_factory=TelegramConfig)
    extract: ExtractOptions = field(default_factory=ExtractOptions)

    @classmethod
    def from_env(cls) -> "AppConfig":
        """Load config from environment variables."""
        return cls(
            github=GitHubConfig(
                username=os.getenv("GITHUB_USERNAME", ""),
                token=os.getenv("GITHUB_TOKEN", ""),
                repo_name=os.getenv("REPO_NAME", "my-uploaded-code"),
                branch=os.getenv("BRANCH", "main"),
                overwrite_branch=os.getenv("OVERWRITE_BRANCH", "true").lower() == "true",
                target_subdir=os.getenv("TARGET_SUBDIR", ""),
                private_repo=os.getenv("PRIVATE_REPO", "false").lower() == "true",
                custom_commit_msg=os.getenv("CUSTOM_COMMIT_MSG", ""),
            ),
            email=EmailConfig(
                enabled=os.getenv("SEND_EMAIL", "false").lower() == "true",
                to=os.getenv("EMAIL_TO", ""),
                sender=os.getenv("EMAIL_FROM", ""),
                password=os.getenv("EMAIL_PASSWORD", ""),
                smtp_server=os.getenv("SMTP_SERVER", "smtp.gmail.com"),
                smtp_port=int(os.getenv("SMTP_PORT", "465")),
            ),
            telegram=TelegramConfig(
                bot_token=os.getenv("TELEGRAM_BOT_TOKEN", ""),
                chat_id=os.getenv("TELEGRAM_CHAT_ID", ""),
            ),
            extract=ExtractOptions(),
        )
