import uuid6
import uuid
from datetime import datetime

from sqlalchemy import String, DateTime, JSON, text
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from .base import Base


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid6.uuid7
    )

    prompt: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String, server_default=text("'queued'"), default="queued")
    canonical_result: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now(),nullable=False) 