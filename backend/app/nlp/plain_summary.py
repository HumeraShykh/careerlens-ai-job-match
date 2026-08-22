from __future__ import annotations

from app.nlp.preprocess import extract_years_of_experience, word_count
from app.nlp.skills import ExtractedSkill


def simple_match_title(score: float) -> str:
    if score >= 80:
        return "Strong match"
    if score >= 65:
        return "Good match"
    if score >= 45:
        return "Okay match"
    return "Weak match"


def simple_match_blurb(score: float) -> str:
    if score >= 80:
        return "Your resume already covers most of what this job is asking for."
    if score >= 65:
        return "Many skills match. A few clear edits can make the resume fit better."
    if score >= 45:
        return "Some skills match, but the resume still misses important parts of this job."
    return "The resume and this job do not look very close yet."


def experience_advice(resume_text: str, job_text: str) -> str:
    job_years = extract_years_of_experience(job_text)
    resume_years = extract_years_of_experience(resume_text)
    if job_years is None:
        return "This job did not clearly say how many years of experience it wants."
    if resume_years is None:
        return (
            f"This job wants about {int(job_years)}+ years of experience. "
            "Your resume does not clearly show years — add them if you have them."
        )
    if resume_years >= job_years:
        return (
            f"Experience looks enough. This job wants about {int(job_years)}+ years. "
            f"Your resume shows about {int(resume_years)} years."
        )
    return (
        f"This job wants about {int(job_years)}+ years of experience. "
        f"Your resume shows about {int(resume_years)} years. "
        "Add more of the work they asked for, but only if it is true."
    )


def improve_tips(
    missing_skills: list[ExtractedSkill],
    job_too_short: bool,
    experience_text: str,
) -> list[str]:
    tips: list[str] = []
    if job_too_short:
        tips.append("Paste the full job posting. A very short job text gives a weak, confusing result.")
    missing_names = [skill.name for skill in missing_skills if skill.category != "soft"][:5]
    if missing_names:
        tips.append("If you really have these skills, add them clearly: " + ", ".join(missing_names) + ".")
    if "looks enough" not in experience_text:
        tips.append(experience_text)
    if not tips:
        tips.append("Keep the facts honest. Use the job's skill names only for work you have actually done.")
    unique: list[str] = []
    for tip in tips:
        if tip not in unique:
            unique.append(tip)
    return unique[:3]


def build_plain_summary(
    resume_text: str,
    job_text: str,
    matched_skills: list[ExtractedSkill],
    missing_skills: list[ExtractedSkill],
    overall_score: float,
) -> dict:
    job_too_short = word_count(job_text) < 80
    experience = experience_advice(resume_text, job_text)
    return {
        "match_title": simple_match_title(overall_score),
        "match_blurb": simple_match_blurb(overall_score),
        "job_too_short": job_too_short,
        "experience": experience,
        "improve": improve_tips(missing_skills, job_too_short, experience),
        "matched_names": [skill.name for skill in matched_skills],
        "missing_names": [skill.name for skill in missing_skills],
    }
