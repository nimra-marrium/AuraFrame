"""
Shared logger factory. Every module gets its own named logger (e.g.
"auraframe.boards", "auraframe.auth") so log lines show exactly which
module something happened in - no more guessing from a bare traceback.

Usage in any service.py:
    from app.core.logging import get_logger
    logger = get_logger(__name__)

    def save(...):
        try:
            ...
        except Exception as e:
            logger.error(f"Failed to save board for project {project_id}: {e}")
            raise ValueError("failed to save board") from e
"""
import logging


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(f"auraframe.{name.split('.')[-2]}")