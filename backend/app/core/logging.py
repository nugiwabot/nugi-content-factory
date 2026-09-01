import logging
import sys
from typing import Any, Dict
from app.core.config import settings


def setup_logging() -> logging.Logger:
    """
    Configures structured standard logging for the application.
    Masks secrets and provides clear component attribution.
    """
    log_level = logging.DEBUG if settings.DEBUG else logging.INFO

    # Custom Formatter
    formatter = logging.Formatter(
        fmt="[%(asctime)s] [%(levelname)s] [%(name)s:%(lineno)d] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Console Handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    handler.setLevel(log_level)

    # Root Logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Remove existing handlers to avoid duplicates
    for existing_handler in root_logger.handlers[:]:
        root_logger.removeHandler(existing_handler)

    root_logger.addHandler(handler)

    # Suppress verbose 3rd party logs
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

    logger = logging.getLogger("nugi_content_factory")
    logger.info(f"Logging initialized in {settings.APP_ENV} mode (Level: {logging.getLevelName(log_level)})")
    return logger


logger = logging.getLogger("nugi_content_factory")
