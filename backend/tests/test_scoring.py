from app.core.scoring_weights import SCORE_WEIGHTS, interpret_score
from app.nlp.scoring import score_keywords, score_skills
from app.nlp.skills import ExtractedSkill
from app.services.analysis_service import analyze_documents


def _skill(name: str) -> ExtractedSkill:
    return ExtractedSkill(name=name, category="language", matched_on=name, frequency=1)


def test_weights_sum_to_one() -> None:
    assert round(sum(SCORE_WEIGHTS.values()), 2) == 1.0


def test_skill_score_is_job_coverage() -> None:
    job = [_skill("Python"), _skill("React"), _skill("SQL"), _skill("Docker")]
    matched = [_skill("Python"), _skill("React")]
    assert score_skills(matched, job) == 50.0


def test_keyword_score_is_weighted() -> None:
    keywords = [
        {"term": "react", "relevance": 0.8, "in_resume": True},
        {"term": "kubernetes", "relevance": 0.2, "in_resume": False},
    ]
    assert score_keywords(keywords) == 80.0


def test_interpret_score_thresholds() -> None:
    assert interpret_score(82) == "Excellent alignment"
    assert interpret_score(70) == "Strong alignment"
    assert interpret_score(50) == "Moderate alignment"
    assert interpret_score(20) == "Needs improvement"


def test_strong_resume_scores_higher_than_unrelated_resume() -> None:
    job = (
        "Software Engineer using React, TypeScript, Node.js, REST APIs, PostgreSQL, "
        "Git, and unit testing. 3+ years of professional software engineering experience. "
        "Bachelor's degree in Computer Science or equivalent practical experience. "
        "You will build user-facing features, write tests, review pull requests, "
        "and collaborate with design and product on a customer workspace platform."
    )
    strong = (
        "Jordan Hale. 4 years of professional software engineering experience. "
        "Built React and TypeScript dashboards, designed Node.js REST APIs, "
        "modeled data in PostgreSQL, used Git and code review, and wrote unit testing. "
        "Bachelor's B.S. Computer Science."
    )
    weak = (
        "Alex Morgan is a pastry chef who managed a bakery, decorated cakes, "
        "and taught weekend frosting workshops for five years."
    )
    strong_score = analyze_documents(strong, job)["breakdown"]["overall"]
    weak_score = analyze_documents(weak, job)["breakdown"]["overall"]
    assert strong_score > weak_score
    assert strong_score >= 65
    assert weak_score < 45
    summary = analyze_documents(strong, job)["plain_summary"]
    assert "3" in summary["experience"]
    assert "4" in summary["experience"]
    assert "React" in summary["matched_names"]
