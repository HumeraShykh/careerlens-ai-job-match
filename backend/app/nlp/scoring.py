from __future__ import annotations

from app.core.scoring_weights import (
    COMPONENT_HELP,
    COMPONENT_LABELS,
    MISSING_EDUCATION_REQUIREMENT_SCORE,
    SCORE_WEIGHTS,
    interpret_score,
)
from app.nlp.extractors import extract_education_signals, extract_experience_signals
from app.nlp.preprocess import extract_years_of_experience
from app.nlp.skills import ExtractedSkill
from app.nlp.similarity import tfidf_cosine_similarity


def _clamp(value: float) -> float:
    return max(0.0, min(100.0, value))


def score_skills(matched: list[ExtractedSkill], job_skills: list[ExtractedSkill]) -> float:
    if not job_skills:
        return 70.0
    return _clamp(100.0 * len(matched) / len(job_skills))


def score_keywords(keywords: list[dict]) -> float:
    if not keywords:
        return 0.0
    weighted_hits = 0.0
    weighted_total = 0.0
    for item in keywords:
        weight = max(item.get("relevance", 0.0), 0.01)
        weighted_total += weight
        if item.get("in_resume"):
            weighted_hits += weight
    return _clamp(100.0 * weighted_hits / weighted_total)


def score_experience(resume_text: str, job_text: str) -> float:
    job_years = extract_years_of_experience(job_text)
    resume_years = extract_years_of_experience(resume_text)
    years_score = 70.0
    if job_years is not None:
        if resume_years is None:
            years_score = 45.0
        elif resume_years >= job_years:
            years_score = 100.0
        else:
            years_score = _clamp(100.0 * (resume_years / job_years))

    job_signals = extract_experience_signals(job_text)
    resume_signals = extract_experience_signals(resume_text)
    job_cues = set(job_signals["action_cues"])
    if job_cues:
        cue_score = 100.0 * len(job_cues.intersection(resume_signals["action_cues"])) / len(job_cues)
    else:
        cue_score = 65.0 if resume_signals["action_cues"] else 40.0

    seniority_bonus = 0.0
    job_seniority = set(job_signals["seniority"])
    resume_seniority = set(resume_signals["seniority"])
    if job_seniority and job_seniority.intersection(resume_seniority):
        seniority_bonus = 8.0

    return _clamp((years_score * 0.55) + (cue_score * 0.45) + seniority_bonus)


def score_education(resume_text: str, job_text: str) -> float:
    job_edu = extract_education_signals(job_text)
    resume_edu = extract_education_signals(resume_text)
    if not job_edu["mentioned"]:
        return MISSING_EDUCATION_REQUIREMENT_SCORE
    job_phrases = set(job_edu["phrases"])
    resume_phrases = set(resume_edu["phrases"])
    if not job_phrases:
        return MISSING_EDUCATION_REQUIREMENT_SCORE
    overlap = job_phrases.intersection(resume_phrases)
    return _clamp(100.0 * len(overlap) / len(job_phrases))


def build_breakdown(
    resume_text: str,
    job_text: str,
    matched_skills: list[ExtractedSkill],
    job_skills: list[ExtractedSkill],
    keywords: list[dict],
) -> dict:
    components = {
        "skills_match": round(score_skills(matched_skills, job_skills), 1),
        "keyword_coverage": round(score_keywords(keywords), 1),
        "experience_relevance": round(score_experience(resume_text, job_text), 1),
        "education_coverage": round(score_education(resume_text, job_text), 1),
        "text_similarity": round(tfidf_cosine_similarity(resume_text, job_text), 1),
    }
    overall = sum(components[key] * SCORE_WEIGHTS[key] for key in SCORE_WEIGHTS)
    overall = round(_clamp(overall), 1)
    return {
        "overall": overall,
        "interpretation": interpret_score(overall),
        "weights": dict(SCORE_WEIGHTS),
        "components": [
            {
                "key": key,
                "label": COMPONENT_LABELS[key],
                "score": components[key],
                "weight": SCORE_WEIGHTS[key],
                "help": COMPONENT_HELP[key],
            }
            for key in SCORE_WEIGHTS
        ],
    }
