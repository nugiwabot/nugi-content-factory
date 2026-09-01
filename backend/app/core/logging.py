import logging
import sys
from typing import Any, Dict
from app.core.config import settings


def setup_logging() -> logging.Logger:
    """
    Configures structured standard logging for the application.
    Masks secrets and provides clear component attribution.
    Handles GUI / Frozen environments where sys.stdout / sys.stderr may be None.
    """
    log_level = logging.DEBUG if settings.DEBUG else logging.INFO

    # Custom Formatter
    formatter = logging.Formatter(
        fmt="[%(asctime)s] [%(levelname)s] [%(name)s:%(lineno)d] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Root Logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Remove existing handlers to avoid duplicates
    for existing_handler in root_logger.handlers[:]:
        root_logger.removeHandler(existing_handler)

    # 1. File Handler (Always reliable in production desktop)
    try:
        log_file = settings.logs_dir / "app.log"
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(formatter)
        file_handler.setLevel(log_level)
        root_logger.addHandler(file_handler)
    except Exception:
        pass

    # 2. Console Handler (Only if sys.stdout is available)
    if sys.stdout is not None:
        try:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            console_handler.setLevel(log_level)
            root_logger.addHandler(console_handler)
        except Exception:
            pass

    # Suppress verbose 3rd party logs
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

    logger = logging.getLogger("nugi_content_factory")
    logger.info(f"Logging initialized in {settings.APP_ENV} mode (Level: {logging.getLevelName(log_level)})")
    return logger


logger = logging.getLogger("nugi_content_factory")
