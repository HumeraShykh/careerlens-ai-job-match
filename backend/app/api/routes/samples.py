from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, HTTPException

router = APIRouter(tags=["samples"])

SAMPLES_DIR = Path(__file__).resolve().parents[4] / "samples"


@router.get("/api/samples")
def list_samples() -> dict:
    resume = SAMPLES_DIR / "sample-resume.txt"
    job = SAMPLES_DIR / "sample-job-description.txt"
    if not resume.exists() or not job.exists():
        raise HTTPException(status_code=404, detail={"error": "Sample files are missing.", "code": "not_found"})
    return {
        "resume": {
            "filename": resume.name,
            "text": resume.read_text(encoding="utf-8"),
        },
        "job_description": {
            "filename": job.name,
            "text": job.read_text(encoding="utf-8"),
        },
    }
