from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.db.session import database_status, get_session
from app.schemas.analysis import SaveAnalysisRequest, SavedAnalysisOut
from app.services.storage import (
    StorageUnavailable,
    delete_analysis,
    get_analysis,
    list_analyses,
    save_analysis,
)

router = APIRouter(tags=["history"])


def _record_to_out(record) -> SavedAnalysisOut:
    return SavedAnalysisOut(
        id=record.id,
        created_at=record.created_at,
        label=record.label,
        job_title_guess=record.job_title_guess,
        source_filename=record.source_filename,
        overall_score=record.overall_score,
        interpretation=record.interpretation,
        resume_word_count=record.resume_word_count,
        job_preview=record.job_preview,
        result=record.result_json,
    )


@router.post("/api/analyses", response_model=SavedAnalysisOut, status_code=201)
def create_analysis(payload: SaveAnalysisRequest, session: Session = Depends(get_session)) -> SavedAnalysisOut:
    try:
        record = save_analysis(session, payload.model_dump())
    except StorageUnavailable as exc:
        raise HTTPException(status_code=503, detail={"error": str(exc), "code": "database_unavailable"}) from exc
    return _record_to_out(record)


@router.get("/api/analyses", response_model=list[SavedAnalysisOut])
def read_analyses(session: Session = Depends(get_session)) -> list[SavedAnalysisOut]:
    if not database_status()["available"]:
        raise HTTPException(
            status_code=503,
            detail={"error": "PostgreSQL is not connected.", "code": "database_unavailable"},
        )
    return [_record_to_out(record) for record in list_analyses(session)]


@router.get("/api/analyses/{analysis_id}", response_model=SavedAnalysisOut)
def read_analysis(analysis_id: UUID, session: Session = Depends(get_session)) -> SavedAnalysisOut:
    try:
        record = get_analysis(session, analysis_id)
    except StorageUnavailable as exc:
        raise HTTPException(status_code=503, detail={"error": str(exc), "code": "database_unavailable"}) from exc
    if record is None:
        raise HTTPException(status_code=404, detail={"error": "Analysis not found.", "code": "not_found"})
    return _record_to_out(record)


@router.delete("/api/analyses/{analysis_id}", status_code=204)
def remove_analysis(analysis_id: UUID, session: Session = Depends(get_session)) -> Response:
    try:
        deleted = delete_analysis(session, analysis_id)
    except StorageUnavailable as exc:
        raise HTTPException(status_code=503, detail={"error": str(exc), "code": "database_unavailable"}) from exc
    if not deleted:
        raise HTTPException(status_code=404, detail={"error": "Analysis not found.", "code": "not_found"})
    return Response(status_code=204)
