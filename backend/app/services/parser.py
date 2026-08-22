from __future__ import annotations

import io
from pathlib import Path

from docx import Document
from pypdf import PdfReader

from app.utils.files import FileValidationError


class ParseError(ValueError):
    def __init__(self, message: str, code: str = "parse_failed") -> None:
        super().__init__(message)
        self.code = code


def extract_text_from_bytes(filename: str, data: bytes) -> str:
    """Extract plain text from an uploaded resume. Never executes file content."""
    suffix = Path(filename).suffix.lower()
    if suffix == ".txt":
        return _decode_text(data)
    if suffix == ".pdf":
        return _extract_pdf(data)
    if suffix == ".docx":
        return _extract_docx(data)
    raise FileValidationError("Unsupported file type.", code="unsupported_type")


def _decode_text(data: bytes) -> str:
    for encoding in ("utf-8", "utf-8-sig", "latin-1"):
        try:
            text = data.decode(encoding)
            if text.strip():
                return text
        except UnicodeDecodeError:
            continue
    raise ParseError("Could not read the text file. Save it as UTF-8 and try again.")


def _extract_pdf(data: bytes) -> str:
    try:
        reader = PdfReader(io.BytesIO(data), strict=False)
    except Exception as exc:  # noqa: BLE001 - library raises mixed exceptions
        raise ParseError("The PDF could not be opened. Try exporting it again.") from exc

    pages: list[str] = []
    for page in reader.pages:
        try:
            pages.append(page.extract_text() or "")
        except Exception:
            continue
    text = "\n".join(pages).strip()
    if not text:
        raise ParseError(
            "No readable text was found in the PDF. Scanned image-only PDFs are not supported yet."
        )
    return text


def _extract_docx(data: bytes) -> str:
    try:
        document = Document(io.BytesIO(data))
    except Exception as exc:  # noqa: BLE001
        raise ParseError("The Word document could not be opened.") from exc
    paragraphs = [paragraph.text.strip() for paragraph in document.paragraphs if paragraph.text.strip()]
    text = "\n".join(paragraphs).strip()
    if not text:
        raise ParseError("The Word document did not contain readable text.")
    return text
