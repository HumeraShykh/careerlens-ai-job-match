from __future__ import annotations

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.nlp.lexicon import STOPWORDS
from app.nlp.preprocess import normalize_text


def tfidf_cosine_similarity(resume_text: str, job_text: str) -> float:
    """Return 0-100 TF-IDF cosine similarity between two documents."""
    left = normalize_text(resume_text)
    right = normalize_text(job_text)
    if not left or not right:
        return 0.0

    vectorizer = TfidfVectorizer(
        stop_words=list(STOPWORDS),
        ngram_range=(1, 2),
        min_df=1,
        token_pattern=r"(?u)\b[a-zA-Z][a-zA-Z0-9+.#/\-]{1,}\b",
    )
    try:
        matrix = vectorizer.fit_transform([left, right])
    except ValueError:
        return 0.0

    if matrix.shape[1] == 0:
        return 0.0
    score = float(cosine_similarity(matrix[0], matrix[1])[0][0])
    return max(0.0, min(100.0, score * 100.0))
