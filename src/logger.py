"""Logging configuration for the project."""

import logging
from src.config import LOG_FORMAT, LOG_LEVEL, LOGS_DIR, LOG_TO_CONSOLE


def setup_logger(name: str, log_file: str = None, console: bool = LOG_TO_CONSOLE) -> logging.Logger:
    """
    Set up a silent-by-default logger with optional console and file handlers.

    Args:
        name: Logger name (typically __name__)
        log_file: Optional log file path
        console: Whether to emit logs to console output

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, LOG_LEVEL))
    logger.propagate = False

    if not logger.handlers:
        logger.addHandler(logging.NullHandler())

    if console and not any(
        isinstance(handler, logging.StreamHandler) and not isinstance(handler, logging.FileHandler)
        for handler in logger.handlers
    ):
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, LOG_LEVEL))
        console_handler.setFormatter(logging.Formatter(LOG_FORMAT))
        logger.addHandler(console_handler)

    if log_file:
        log_path = LOGS_DIR / log_file
        has_file_handler = any(
            isinstance(handler, logging.FileHandler)
            and getattr(handler, "baseFilename", None) == str(log_path)
            for handler in logger.handlers
        )
        if not has_file_handler:
            file_handler = logging.FileHandler(log_path)
            file_handler.setLevel(getattr(logging, LOG_LEVEL))
            file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
            logger.addHandler(file_handler)

    return logger
