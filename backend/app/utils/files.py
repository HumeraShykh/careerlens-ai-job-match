from __future__ import annotations

import re
from pathlib import Path

SAFE_FILENAME_RE = re.compile(r"[^A-Za-z0-9._-]+")

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}
ALLOWED_CONTENT_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/plain",
    "application/octet-stream",
}


class FileValidationError(ValueError):
    def __init__(self, message: str, code: str = "invalid_file") -> None:
        super().__init__(message)
        self.code = code


def sanitize_filename(filename: str) -> str:
    name = Path(filename or "upload").name
    cleaned = SAFE_FILENAME_RE.sub("_", name).strip("._")
    return cleaned or "upload"


def validate_upload(filename: str, content_type: str | None, size: int, max_bytes: int) -> str:
    safe_name = sanitize_filename(filename)
    suffix = Path(safe_name).suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise FileValidationError(
            "Unsupported file type. Upload a PDF, DOCX, or TXT resume.",
            code="unsupported_type",
        )
    if size <= 0:
        raise FileValidationError("The uploaded file is empty.", code="empty_file")
    if size > max_bytes:
        raise FileValidationError(
            f"File is too large. The limit is {max_bytes // (1024 * 1024)} MB.",
            code="file_too_large",
        )
    if content_type and content_type.lower() not in ALLOWED_CONTENT_TYPES:
        # Some browsers send unusual MIME types; extension remains the source of truth.
        if suffix not in ALLOWED_EXTENSIONS:
            raise FileValidationError(
                "Unsupported file type. Upload a PDF, DOCX, or TXT resume.",
                code="unsupported_type",
            )
    return safe_name
