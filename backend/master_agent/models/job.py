import uuid6
import uuid
from datetime import datetime

from sqlalchemy import String, DateTime, text, Integer, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID, JSONB

from .base import Base


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid6.uuid7
    )

    user_id: Mapped[int | None] = mapped_column(Integer, nullable=True)

    prompt_original: Mapped[str] = mapped_column(String, nullable=False)
    prompt_normalized: Mapped[str] = mapped_column(String, nullable=False)

    molecule: Mapped[str | None] = mapped_column(String, nullable=True)
    indications_requested: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    status: Mapped[str] = mapped_column(
        String, 
        server_default=text("'queued'"), 
        default="queued", 
        nullable=False
    )

    canonical_result: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    ) 

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default= func.now(),
        onupdate=func.now(),
        nullable=False
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    synthesis_version: Mapped[str | None] = mapped_column(String, nullable=True)
    data_completeness_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    confidence_overall: Mapped[float | None] = mapped_column(Float, nullable=True)