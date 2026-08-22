from __future__ import annotations

from dataclasses import dataclass

from app.nlp.lexicon import SKILL_TERMS
from app.nlp.preprocess import contains_phrase, count_phrase, normalize_text


@dataclass(frozen=True)
class ExtractedSkill:
    name: str
    category: str
    matched_on: str
    frequency: int


def _is_safe_phrase(phrase: str) -> bool:
    """Ignore tiny word aliases such as 'go' or 'r' that collide with English."""
    compact = phrase.strip().lower()
    if any(symbol in compact for symbol in ("#", "+", ".")):
        return True
    return len(compact) >= 3


def _candidate_phrases(term) -> tuple[str, ...]:
    return tuple(phrase for phrase in (term.name, *term.aliases) if _is_safe_phrase(phrase))


def extract_skills(text: str) -> list[ExtractedSkill]:
    """Extract known skills from free text using the curated lexicon."""
    normalized = normalize_text(text)
    found: list[ExtractedSkill] = []
    for term in SKILL_TERMS:
        best_alias = ""
        best_count = 0
        for alias in _candidate_phrases(term):
            count = count_phrase(normalized, alias)
            if count > best_count:
                best_count = count
                best_alias = alias
        if best_count > 0:
            found.append(
                ExtractedSkill(
                    name=term.name,
                    category=term.category,
                    matched_on=best_alias,
                    frequency=best_count,
                )
            )
    return found


def skill_names(skills: list[ExtractedSkill]) -> list[str]:
    return [skill.name for skill in skills]


def compare_skills(
    resume_skills: list[ExtractedSkill],
    job_skills: list[ExtractedSkill],
) -> tuple[list[ExtractedSkill], list[ExtractedSkill]]:
    resume_names = {skill.name for skill in resume_skills}
    matched = [skill for skill in job_skills if skill.name in resume_names]
    missing = [skill for skill in job_skills if skill.name not in resume_names]
    return matched, missing


def has_skill_mention(text: str, skill_name: str) -> bool:
    normalized = normalize_text(text)
    for term in SKILL_TERMS:
        if term.name.lower() != skill_name.lower():
            continue
        return any(contains_phrase(normalized, alias) for alias in (term.name, *term.aliases))
    return contains_phrase(normalized, skill_name)
