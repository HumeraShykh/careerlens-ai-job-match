from __future__ import annotations

import re
import unicodedata

WHITESPACE_RE = re.compile(r"\s+")
NON_ALNUM_RE = re.compile(r"[^a-z0-9+.#/\- ]+")
YEAR_RE = re.compile(r"(\d+(?:\.\d+)?)\s*\+?\s*(?:years|year|yrs|yr)\b", re.IGNORECASE)
YEAR_RANGE_RE = re.compile(
    r"(?P<start>(?:19|20)\d{2})\s*(?:[–\-]|to)\s*(?P<end>present|(?:19|20)\d{2})",
    re.IGNORECASE,
)
SECTION_HEADING_RE = re.compile(
    r"^(summary|profile|objective|skills|technical skills|experience|work experience|"
    r"employment|education|projects|certifications|awards)[:\s]*$",
    re.IGNORECASE,
)


def normalize_text(text: str) -> str:
    """Lowercase, strip accents, collapse whitespace, and keep useful symbols."""
    if not text:
        return ""
    decomposed = unicodedata.normalize("NFKD", text)
    without_marks = "".join(ch for ch in decomposed if not unicodedata.combining(ch))
    lowered = without_marks.lower()
    cleaned = NON_ALNUM_RE.sub(" ", lowered)
    # Keep dots inside tokens such as node.js, but drop trailing punctuation.
    cleaned = re.sub(r"\.(?![a-z0-9])", " ", cleaned)
    return WHITESPACE_RE.sub(" ", cleaned).strip()


def tokenize(text: str) -> list[str]:
    normalized = normalize_text(text)
    if not normalized:
        return []
    return [token for token in normalized.split(" ") if token]


def word_count(text: str) -> int:
    return len(tokenize(text))


def extract_years_of_experience(text: str) -> float | None:
    matches = YEAR_RE.findall(text or "")
    stated = [float(match) for match in matches]
    sections = split_sections(text or "")
    experience_blob = (
        sections.get("experience")
        or sections.get("work experience")
        or sections.get("employment")
        or (text or "")
    )
    ranged = _years_from_date_ranges(experience_blob)
    values = stated + ranged
    if not values:
        return None
    return max(values)


def _years_from_date_ranges(text: str) -> list[float]:
    from datetime import date

    current_year = date.today().year
    found: list[float] = []
    for match in YEAR_RANGE_RE.finditer(text):
        start = int(match.group("start"))
        end_raw = match.group("end").lower()
        end = current_year if end_raw == "present" else int(end_raw)
        span = max(0, end - start)
        if span > 0:
            found.append(float(span))
    return found


def split_sections(text: str) -> dict[str, str]:
    """Best-effort resume section splitter based on common headings."""
    sections: dict[str, list[str]] = {}
    current = "body"
    sections[current] = []
    for raw_line in (text or "").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        heading_match = SECTION_HEADING_RE.match(line)
        if heading_match:
            current = heading_match.group(1).lower()
            sections.setdefault(current, [])
            continue
        sections[current].append(line)
    return {name: "\n".join(lines) for name, lines in sections.items() if lines}


def contains_phrase(normalized_haystack: str, phrase: str) -> bool:
    """Return True if phrase appears with word-ish boundaries."""
    escaped = re.escape(normalize_text(phrase))
    if not escaped:
        return False
    pattern = rf"(?<![\w+.#]){escaped}(?![\w+.#])"
    return re.search(pattern, normalized_haystack) is not None


def count_phrase(normalized_haystack: str, phrase: str) -> int:
    escaped = re.escape(normalize_text(phrase))
    if not escaped:
        return 0
    pattern = rf"(?<![\w+.#]){escaped}(?![\w+.#])"
    return len(re.findall(pattern, normalized_haystack))
