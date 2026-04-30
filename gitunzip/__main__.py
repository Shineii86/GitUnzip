"""CLI entry point for GitUnzip."""

import logging
import sys

from .config import AppConfig

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("gitunzip")


def run():
    """Run GitUnzip from environment variables."""
    config = AppConfig.from_env()

    if not config.github.token:
        logger.error("GITHUB_TOKEN is required.")
        sys.exit(1)
    if not config.github.username:
        logger.error("GITHUB_USERNAME is required.")
        sys.exit(1)

    from .core import process_uploads
    process_uploads(config)


if __name__ == "__main__":
    run()
