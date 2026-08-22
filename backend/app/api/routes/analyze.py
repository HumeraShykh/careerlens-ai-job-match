from __future__ import annotations

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.core.config import get_settings
from app.schemas.analysis import AnalysisResult, ComparedJobOut, CompareResult
from app.services.analysis_service import AnalysisValidationError, analyze_documents, compare_documents
from app.services.parser import ParseError, extract_text_from_bytes
from app.utils.files import FileValidationError, validate_upload

router = APIRouter(tags=["analyze"])


async def extract_resume_text(
    resume_file: UploadFile | None,
    resume_text: str | None,
) -> tuple[str, str | None]:
    settings = get_settings()
    filename: str | None = None
    extracted = (resume_text or "").strip()

    if resume_file is not None and resume_file.filename:
        data = await resume_file.read()
        try:
            filename = validate_upload(
                resume_file.filename,
                resume_file.content_type,
                len(data),
                settings.max_upload_bytes,
            )
            extracted = extract_text_from_bytes(filename, data)
        except FileValidationError as exc:
            raise HTTPException(status_code=400, detail={"error": str(exc), "code": exc.code}) from exc
        except ParseError as exc:
            raise HTTPException(status_code=422, detail={"error": str(exc), "code": exc.code}) from exc
        finally:
            await resume_file.close()
    return extracted, filename


@router.post("/api/analyze", response_model=AnalysisResult)
async def analyze(
    job_description: str = Form(...),
    resume_text: str | None = Form(default=None),
    resume_file: UploadFile | None = File(default=None),
) -> AnalysisResult:
    extracted, filename = await extract_resume_text(resume_file, resume_text)
    try:
        result = analyze_documents(extracted, job_description, source_filename=filename)
    except AnalysisValidationError as exc:
        raise HTTPException(status_code=400, detail={"error": str(exc), "code": exc.code}) from exc
    return AnalysisResult.model_validate(result)


@router.post("/api/compare", response_model=CompareResult)
async def compare(
    job_description_1: str = Form(...),
    job_description_2: str = Form(...),
    job_description_3: str | None = Form(default=None),
    resume_text: str | None = Form(default=None),
    resume_file: UploadFile | None = File(default=None),
) -> CompareResult:
    extracted, filename = await extract_resume_text(resume_file, resume_text)
    jobs = [("Job 1", job_description_1), ("Job 2", job_description_2)]
    if job_description_3 and job_description_3.strip():
        jobs.append(("Job 3", job_description_3))

    try:
        payload = compare_documents(extracted, jobs, source_filename=filename)
    except AnalysisValidationError as exc:
        raise HTTPException(
            status_code=400,
            detail={"error": str(exc), "code": exc.code},
        ) from exc

    return CompareResult(
        winner_label=payload["winner_label"],
        winner_title=payload["winner_title"],
        summary=payload["summary"],
        jobs=[ComparedJobOut.model_validate(item) for item in payload["jobs"]],
    )
