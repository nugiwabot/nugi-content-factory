import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime
from app.database import Base


def generate_uuid() -> str:
    """Generates a standard 36-char string UUIDv4."""
    return str(uuid.uuid4())


def utc_now() -> datetime:
    """Returns timezone-aware UTC datetime."""
    return datetime.now(timezone.utc)


class BaseModel(Base):
    """
    Abstract base model providing standardized UUID primary keys and timestamps.
    """
    __abstract__ = True

    id = Column(String(36), primary_key=True, default=generate_uuid, index=True)
    created_at = Column(DateTime, default=utc_now, nullable=False)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now, nullable=False)
