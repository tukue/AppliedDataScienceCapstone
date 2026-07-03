"""Logging configuration for the project."""

import logging
from pathlib import Path
from src.config import LOG_FORMAT, LOG_LEVEL, LOGS_DIR


def setup_logger(name: str, log_file: str = None) -> logging.Logger:
    """
    Set up a logger with console and optional file handlers.
    
    Args:
        name: Logger name (typically __name__)
        log_file: Optional log file path
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, LOG_LEVEL))
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, LOG_LEVEL))
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    logger.addHandler(console_handler)
    
    # File handler (optional)
    if log_file:
        log_path = LOGS_DIR / log_file
        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(getattr(logging, LOG_LEVEL))
        file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
        logger.addHandler(file_handler)
    
    return logger
