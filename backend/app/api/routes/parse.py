from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.core.config import get_settings
from app.nlp.preprocess import word_count
from app.schemas.analysis import ParseResponse
from app.services.parser import ParseError, extract_text_from_bytes
from app.utils.files import FileValidationError, validate_upload

router = APIRouter(tags=["parse"])


@router.post("/api/parse/resume", response_model=ParseResponse)
async def parse_resume(file: UploadFile = File(...)) -> ParseResponse:
    settings = get_settings()
    data = await file.read()
    try:
        filename = validate_upload(
            file.filename or "resume.txt",
            file.content_type,
            len(data),
            settings.max_upload_bytes,
        )
        text = extract_text_from_bytes(filename, data)
    except FileValidationError as exc:
        raise HTTPException(status_code=400, detail={"error": str(exc), "code": exc.code}) from exc
    except ParseError as exc:
        raise HTTPException(status_code=422, detail={"error": str(exc), "code": exc.code}) from exc
    finally:
        await file.close()

    return ParseResponse(
        filename=filename,
        file_type=Path(filename).suffix.lower().lstrip("."),
        file_size=len(data),
        word_count=word_count(text),
        text=text,
    )
