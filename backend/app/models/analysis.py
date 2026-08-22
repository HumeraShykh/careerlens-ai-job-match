from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class AnalysisRecord(Base):
    """Saved analysis metadata. Raw resume files are never stored."""

    __tablename__ = "analyses"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    label: Mapped[str | None] = mapped_column(String(160), nullable=True)
    job_title_guess: Mapped[str | None] = mapped_column(String(160), nullable=True)
    source_filename: Mapped[str | None] = mapped_column(String(255), nullable=True)
    overall_score: Mapped[float] = mapped_column(Float, nullable=False)
    interpretation: Mapped[str] = mapped_column(String(64), nullable=False)
    resume_word_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    job_preview: Mapped[str | None] = mapped_column(String(240), nullable=True)
    result_json: Mapped[dict] = mapped_column(JSONB, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
