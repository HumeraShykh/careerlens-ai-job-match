"""Transparent, documented scoring weights for CareerLens AI.

These weights are CareerLens AI's own relevance model. They are not an
employer ATS score and must be shown as such in the product UI.
"""

from typing import TypedDict


class ScoreWeights(TypedDict):
    skills_match: float
    keyword_coverage: float
    experience_relevance: float
    education_coverage: float
    text_similarity: float


SCORE_WEIGHTS: ScoreWeights = {
    "skills_match": 0.35,
    "keyword_coverage": 0.25,
    "experience_relevance": 0.15,
    "education_coverage": 0.10,
    "text_similarity": 0.15,
}

ALIGNMENT_THRESHOLDS = {
    "excellent": 80,
    "strong": 65,
    "moderate": 45,
}

# If a job description never mentions education, this component should not
# punish the candidate. Neutral credit keeps the overall score honest.
MISSING_EDUCATION_REQUIREMENT_SCORE = 70.0

COMPONENT_LABELS = {
    "skills_match": "Skills Match",
    "keyword_coverage": "Keyword Coverage",
    "experience_relevance": "Experience Relevance",
    "education_coverage": "Education Coverage",
    "text_similarity": "Text Similarity",
}

COMPONENT_HELP = {
    "skills_match": "Share of job-description skills that also appear in the resume, using CareerLens skill aliases.",
    "keyword_coverage": "How many important job-description terms (beyond stopwords) also appear in the resume.",
    "experience_relevance": "Overlap of experience language, seniority cues, and stated years of experience.",
    "education_coverage": "Whether degree or field requirements from the job description appear in the resume.",
    "text_similarity": "TF-IDF cosine similarity between the full resume text and the job description.",
}


def interpret_score(score: float) -> str:
    if score >= ALIGNMENT_THRESHOLDS["excellent"]:
        return "Excellent alignment"
    if score >= ALIGNMENT_THRESHOLDS["strong"]:
        return "Strong alignment"
    if score >= ALIGNMENT_THRESHOLDS["moderate"]:
        return "Moderate alignment"
    return "Needs improvement"
