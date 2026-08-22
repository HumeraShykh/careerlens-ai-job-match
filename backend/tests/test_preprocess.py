from app.nlp.preprocess import (
    contains_phrase,
    extract_years_of_experience,
    normalize_text,
    tokenize,
    word_count,
)


def test_normalize_collapses_whitespace_and_case() -> None:
    assert normalize_text("  React\nEngineer  ") == "react engineer"


def test_tokenize_drops_empty_tokens() -> None:
    assert tokenize("Python, React, and SQL.") == ["python", "react", "and", "sql"]


def test_word_count() -> None:
    assert word_count("one two three") == 3
    assert word_count("") == 0


def test_contains_phrase_uses_boundaries() -> None:
    assert contains_phrase("skilled in java and python", "java")
    assert not contains_phrase("skilled in javascript", "java")


def test_extract_years_picks_highest_mentioned() -> None:
    text = "2 years in internships and 4 years of professional software engineering"
    assert extract_years_of_experience(text) == 4.0
    assert extract_years_of_experience("no numbers here") is None
