from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import database_status
from app.models.analysis import AnalysisRecord


class StorageUnavailable(RuntimeError):
    def __init__(self, message: str = "Saving history requires PostgreSQL.") -> None:
        super().__init__(message)


def require_database() -> None:
    status = database_status()
    if not status["available"]:
        raise StorageUnavailable(
            "Analysis history is unavailable because PostgreSQL is not connected. "
            "You can still analyze without saving."
        )


def save_analysis(session: Session, payload: dict) -> AnalysisRecord:
    require_database()
    result = payload["result"]
    record = AnalysisRecord(
        label=payload.get("label"),
        job_title_guess=result.get("job_title_guess"),
        source_filename=result.get("source_filename"),
        overall_score=result["breakdown"]["overall"],
        interpretation=result["breakdown"]["interpretation"],
        resume_word_count=result.get("resume_word_count", 0),
        job_preview=payload.get("job_preview"),
        result_json=result,
    )
    session.add(record)
    session.flush()
    return record


def list_analyses(session: Session, limit: int = 20) -> list[AnalysisRecord]:
    require_database()
    statement = select(AnalysisRecord).order_by(AnalysisRecord.created_at.desc()).limit(limit)
    return list(session.scalars(statement))


def get_analysis(session: Session, analysis_id: UUID) -> AnalysisRecord | None:
    require_database()
    return session.get(AnalysisRecord, analysis_id)


def delete_analysis(session: Session, analysis_id: UUID) -> bool:
    require_database()
    record = session.get(AnalysisRecord, analysis_id)
    if record is None:
        return False
    session.delete(record)
    return True
