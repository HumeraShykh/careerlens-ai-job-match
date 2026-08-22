from __future__ import annotations

import re
from collections import Counter

from sklearn.feature_extraction.text import TfidfVectorizer

from app.nlp.lexicon import DEGREE_PHRASES, EXPERIENCE_CUES, SENIORITY_TERMS, STOPWORDS
from app.nlp.preprocess import contains_phrase, normalize_text, tokenize

JOB_TITLE_RE = re.compile(
    r"^(?P<title>(?:senior |staff |principal |lead |junior )?"
    r"(?:software|full[- ]stack|frontend|front[- ]end|backend|back[- ]end|data|"
    r"machine learning|ml|platform|product)?"
    r"(?:\s+)?(?:engineer|developer|analyst|scientist|designer|manager).*)$",
    re.IGNORECASE,
)


def extract_keywords(job_text: str, resume_text: str, limit: int = 18) -> list[dict]:
    """Rank job-description terms with TF-IDF and mark resume presence."""
    documents = [job_text or "", resume_text or ""]
    if not normalize_text(documents[0]):
        return []

    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words=list(STOPWORDS),
        ngram_range=(1, 2),
        min_df=1,
        token_pattern=r"(?u)\b[a-zA-Z][a-zA-Z0-9+.#/\-]{1,}\b",
    )
    try:
        matrix = vectorizer.fit_transform(documents)
    except ValueError:
        return []

    feature_names = vectorizer.get_feature_names_out()
    job_scores = matrix[0].toarray().ravel()
    ranked = sorted(
        (
            (feature_names[index], float(job_scores[index]))
            for index in range(len(feature_names))
            if job_scores[index] > 0
        ),
        key=lambda item: item[1],
        reverse=True,
    )

    resume_normalized = normalize_text(resume_text)
    keywords: list[dict] = []
    seen = set()
    for term, score in ranked:
        if term in STOPWORDS or term in seen:
            continue
        if len(term) < 3:
            continue
        seen.add(term)
        present = contains_phrase(resume_normalized, term)
        keywords.append(
            {
                "term": term,
                "relevance": round(score, 4),
                "in_resume": present,
                "frequency_in_job": count_raw_term(job_text, term),
            }
        )
        if len(keywords) >= limit:
            break
    return keywords


def count_raw_term(text: str, term: str) -> int:
    tokens = tokenize(text)
    parts = normalize_text(term).split()
    if len(parts) == 1:
        return Counter(tokens)[parts[0]]
    joined = " ".join(tokens)
    return joined.count(" ".join(parts))


def extract_experience_signals(text: str) -> dict:
    normalized = normalize_text(text)
    cues = [cue for cue in EXPERIENCE_CUES if contains_phrase(normalized, cue)]
    seniority = [term for term in SENIORITY_TERMS if contains_phrase(normalized, term)]
    return {"action_cues": cues, "seniority": seniority}


def extract_education_signals(text: str) -> dict:
    normalized = normalize_text(text)
    matches = [phrase for phrase in DEGREE_PHRASES if contains_phrase(normalized, phrase)]
    return {"phrases": matches, "mentioned": bool(matches)}


def guess_job_title(job_text: str) -> str | None:
    for line in (job_text or "").splitlines():
        cleaned = line.strip(" -:\t")
        if len(cleaned) < 6 or len(cleaned) > 80:
            continue
        if JOB_TITLE_RE.match(cleaned):
            return cleaned
    return None
