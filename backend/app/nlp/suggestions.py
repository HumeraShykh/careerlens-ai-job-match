from __future__ import annotations

import re

from app.nlp.preprocess import word_count
from app.nlp.skills import ExtractedSkill

METRIC_RE = re.compile(r"(\d+\s*%|\$\s*\d|\d{2,}|reduced|increased|improved)", re.IGNORECASE)
WEAK_PHRASE_RE = re.compile(
    r"\b(worked on|helped with|responsible for|involved in)\b",
    re.IGNORECASE,
)


def build_suggestions(
    resume_text: str,
    missing_skills: list[ExtractedSkill],
    keywords: list[dict],
    breakdown: dict,
) -> list[dict]:
    suggestions: list[dict] = []
    words = word_count(resume_text)

    high_value_missing = [skill.name for skill in missing_skills if skill.category != "soft"][:6]
    if high_value_missing:
        suggestions.append(
            {
                "title": "Surface skills you actually have",
                "detail": (
                    "The job description emphasizes "
                    + ", ".join(high_value_missing)
                    + ". Add them only if you can discuss them honestly in an interview."
                ),
                "kind": "skills",
            }
        )

    missing_keywords = [item["term"] for item in keywords if not item["in_resume"]][:5]
    if missing_keywords:
        suggestions.append(
            {
                "title": "Mirror important job language when it is truthful",
                "detail": (
                    "These job keywords did not appear clearly in the resume: "
                    + ", ".join(missing_keywords)
                    + ". Use the employer's wording only for work you have done."
                ),
                "kind": "keywords",
            }
        )

    if words < 180:
        suggestions.append(
            {
                "title": "The resume is quite short",
                "detail": (
                    f"CareerLens counted about {words} words. Adding concrete project or "
                    "role detail usually helps keyword coverage more than repeating a skill list."
                ),
                "kind": "structure",
            }
        )
    elif words > 900:
        suggestions.append(
            {
                "title": "Tighten long sections",
                "detail": (
                    f"CareerLens counted about {words} words. A focused one-to-two page resume "
                    "is easier for both people and parsers to scan."
                ),
                "kind": "structure",
            }
        )

    if not METRIC_RE.search(resume_text or ""):
        suggestions.append(
            {
                "title": "Add measurable scope when you have it",
                "detail": (
                    "No clear numbers, percentages, or impact verbs were detected. "
                    "If you have them, prefer 'reduced API latency from 420ms to 180ms' "
                    "over 'worked on APIs'."
                ),
                "kind": "impact",
            }
        )
    elif WEAK_PHRASE_RE.search(resume_text or ""):
        suggestions.append(
            {
                "title": "Replace vague duty language",
                "detail": (
                    "Phrases such as 'worked on' or 'responsible for' are weaker than "
                    "verbs that name the outcome. Keep the facts; sharpen the wording."
                ),
                "kind": "impact",
            }
        )

    education_score = next(
        (item["score"] for item in breakdown["components"] if item["key"] == "education_coverage"),
        100,
    )
    if education_score < 50:
        suggestions.append(
            {
                "title": "Education or equivalent experience is hard to see",
                "detail": (
                    "The job description mentions education or a field of study that is not "
                    "obvious in the resume. If you have equivalent experience, say so explicitly."
                ),
                "kind": "education",
            }
        )

    experience_score = next(
        (item["score"] for item in breakdown["components"] if item["key"] == "experience_relevance"),
        100,
    )
    if experience_score < 50:
        suggestions.append(
            {
                "title": "Make relevant experience easier to find",
                "detail": (
                    "Experience overlap looks limited. Move the most relevant role or project "
                    "near the top and name the products, users, or systems you touched."
                ),
                "kind": "experience",
            }
        )

    if not suggestions:
        suggestions.append(
            {
                "title": "The resume already covers the core requirements",
                "detail": (
                    "Focus on tailoring examples and impact rather than adding extra keywords. "
                    "Do not invent experience to chase a higher score."
                ),
                "kind": "strength",
            }
        )

    suggestions.append(
        {
            "title": "Do not fabricate skills or achievements",
            "detail": (
                "CareerLens AI is a preparation tool. Only add skills, tools, or results you "
                "can defend in an interview."
            ),
            "kind": "ethics",
        }
    )
    return suggestions


def build_strengths(
    matched_skills: list[ExtractedSkill],
    breakdown: dict,
) -> list[str]:
    strengths: list[str] = []
    by_category: dict[str, list[str]] = {}
    for skill in matched_skills:
        by_category.setdefault(skill.category, []).append(skill.name)

    if by_category.get("language"):
        strengths.append("Strong language overlap: " + ", ".join(by_category["language"][:5]) + ".")
    if by_category.get("frontend") or by_category.get("backend"):
        stack = by_category.get("frontend", []) + by_category.get("backend", [])
        strengths.append("Relevant framework or runtime experience: " + ", ".join(stack[:5]) + ".")
    if by_category.get("database"):
        strengths.append("Database alignment: " + ", ".join(by_category["database"][:4]) + ".")
    if by_category.get("testing"):
        strengths.append("Testing practices appear in both documents.")

    overall = breakdown["overall"]
    if overall >= 80:
        strengths.append("Overall language and skill coverage is already in a strong range.")
    elif breakdown["components"][0]["score"] >= 75:
        strengths.append("Most required skills from the job description are already named.")

    return strengths[:5] or ["Some overlapping language was found, but the match is still thin."]


def build_gaps(missing_skills: list[ExtractedSkill], keywords: list[dict], breakdown: dict) -> list[str]:
    gaps: list[str] = []
    important_missing = [skill.name for skill in missing_skills if skill.category in {"language", "frontend", "backend", "database", "data"}]
    if important_missing:
        gaps.append("Not clearly mentioned: " + ", ".join(important_missing[:6]) + ".")
    missing_keywords = [item["term"] for item in keywords if not item["in_resume"]][:4]
    if missing_keywords:
        gaps.append("Job keywords with little resume support: " + ", ".join(missing_keywords) + ".")
    if breakdown["overall"] < 45:
        gaps.append("The documents share limited vocabulary. This may still be a fit if experience is described differently.")
    return gaps[:5] or ["No major wording gaps stood out beyond ordinary tailoring."]
