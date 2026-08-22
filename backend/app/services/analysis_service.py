from __future__ import annotations

from app.nlp.extractors import extract_keywords, guess_job_title
from app.nlp.plain_summary import build_plain_summary
from app.nlp.preprocess import word_count
from app.nlp.scoring import build_breakdown
from app.nlp.skills import compare_skills, extract_skills
from app.nlp.suggestions import build_gaps, build_strengths, build_suggestions


MIN_JOB_DESCRIPTION_CHARS = 40
MIN_RESUME_CHARS = 40


class AnalysisValidationError(ValueError):
    def __init__(self, message: str, code: str = "invalid_input") -> None:
        super().__init__(message)
        self.code = code


def analyze_documents(resume_text: str, job_description: str, source_filename: str | None = None) -> dict:
    resume = (resume_text or "").strip()
    job = (job_description or "").strip()
    if len(resume) < MIN_RESUME_CHARS:
        raise AnalysisValidationError(
            "The resume text is too short to analyze. Upload a fuller resume or paste more content.",
            code="resume_too_short",
        )
    if len(job) < MIN_JOB_DESCRIPTION_CHARS or word_count(job) < 40:
        raise AnalysisValidationError(
            "Please paste the full job posting, including requirements and skills. One short line is not enough.",
            code="job_too_short",
        )

    resume_skills = extract_skills(resume)
    job_skills = extract_skills(job)
    matched, missing = compare_skills(resume_skills, job_skills)
    keywords = extract_keywords(job, resume)
    breakdown = build_breakdown(resume, job, matched, job_skills, keywords)
    plain_summary = build_plain_summary(resume, job, matched, missing, breakdown["overall"])

    return {
        "disclaimer": (
            "This is CareerLens AI's own relevance score, not an employer's official ATS result. "
            "It cannot predict whether an application will be screened in or out."
        ),
        "job_title_guess": guess_job_title(job),
        "source_filename": source_filename,
        "resume_word_count": word_count(resume),
        "job_word_count": word_count(job),
        "breakdown": breakdown,
        "plain_summary": plain_summary,
        "matched_skills": [_skill_payload(skill) for skill in matched],
        "missing_skills": [_skill_payload(skill) for skill in missing],
        "resume_skills": [_skill_payload(skill) for skill in resume_skills],
        "job_skills": [_skill_payload(skill) for skill in job_skills],
        "keywords": keywords,
        "suggestions": build_suggestions(resume, missing, keywords, breakdown),
        "strengths": build_strengths(matched, breakdown),
        "gaps": build_gaps(missing, keywords, breakdown),
    }


def compare_documents(
    resume_text: str,
    jobs: list[tuple[str, str]],
    source_filename: str | None = None,
) -> dict:
    if len(jobs) < 2:
        raise AnalysisValidationError(
            "Paste at least two full job postings to compare.",
            code="need_two_jobs",
        )
    if len(jobs) > 3:
        raise AnalysisValidationError(
            "You can compare up to three jobs at a time.",
            code="too_many_jobs",
        )

    compared: list[dict] = []
    for label, job_text in jobs:
        try:
            result = analyze_documents(resume_text, job_text, source_filename=source_filename)
        except AnalysisValidationError as exc:
            raise AnalysisValidationError(f"{label}: {exc}", code=exc.code) from exc
        summary = result.get("plain_summary") or {}
        compared.append(
            {
                "label": label,
                "rank": 0,
                "is_best": False,
                "job_title_guess": result.get("job_title_guess"),
                "score": result["breakdown"]["overall"],
                "match_title": summary.get("match_title", result["breakdown"]["interpretation"]),
                "experience": summary.get("experience", ""),
                "matched_skills": result["matched_skills"],
                "missing_skills": result["missing_skills"],
                "improve": summary.get("improve", []),
            }
        )

    ranked = sorted(compared, key=lambda item: (-item["score"], item["label"]))
    for index, item in enumerate(ranked, start=1):
        item["rank"] = index
        item["is_best"] = index == 1

    winner = ranked[0]
    winner_name = winner["job_title_guess"] or winner["label"]
    summary_text = f"{winner_name} is the better fit for this resume ({winner['score']:.0f}% match)."
    if len(ranked) > 1:
        second = ranked[1]
        if winner["score"] - second["score"] < 3:
            second_name = second["job_title_guess"] or second["label"]
            summary_text = f"{winner_name} and {second_name} are very close. Either could work."

    return {
        "winner_label": winner["label"],
        "winner_title": winner["job_title_guess"],
        "summary": summary_text,
        "jobs": ranked,
    }


def _skill_payload(skill) -> dict:
    return {
        "name": skill.name,
        "category": skill.category,
        "matched_on": skill.matched_on,
        "frequency": skill.frequency,
    }
