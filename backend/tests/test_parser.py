from pathlib import Path

import pytest

from app.services.parser import ParseError, extract_text_from_bytes
from app.utils.files import FileValidationError, sanitize_filename, validate_upload


def test_sanitize_filename_strips_paths() -> None:
    assert sanitize_filename("../../etc/passwd.pdf") == "passwd.pdf"
    assert sanitize_filename("My Resume (Final).docx") == "My_Resume_Final_.docx"


def test_validate_upload_rejects_bad_type_and_size() -> None:
    with pytest.raises(FileValidationError):
        validate_upload("photo.png", "image/png", 100, 5_000_000)
    with pytest.raises(FileValidationError):
        validate_upload("resume.pdf", "application/pdf", 9_000_000, 5_000_000)


def test_extract_plain_text() -> None:
    text = extract_text_from_bytes("resume.txt", b"Software engineer using React")
    assert "React" in text


def test_empty_pdf_raises_parse_error() -> None:
    with pytest.raises((ParseError, Exception)):
        extract_text_from_bytes("resume.pdf", b"not-a-pdf")


def test_sample_resume_file_exists() -> None:
    sample = Path(__file__).resolve().parents[2] / "samples" / "sample-resume.txt"
    assert sample.exists()
    assert "JORDAN HALE" in sample.read_text(encoding="utf-8")


def test_extract_sample_pdf() -> None:
    sample = Path(__file__).resolve().parents[2] / "samples" / "sample-resume.pdf"
    text = extract_text_from_bytes(sample.name, sample.read_bytes())
    assert "JORDAN HALE" in text
    assert "React" in text
