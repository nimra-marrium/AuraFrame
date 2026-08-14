import logging

def get_logger(module_name: str) -> logging.Logger:
    """Returns a logger instance scoped to a specific module."""
    return logging.getLogger(f"auraframe.{module_name}")