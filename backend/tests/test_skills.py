from app.nlp.skills import compare_skills, extract_skills


def test_extracts_canonical_skills_and_aliases() -> None:
    text = "I use React.js, Node, Postgres, and REST APIs every week."
    names = {skill.name for skill in extract_skills(text)}
    assert "React" in names
    assert "Node.js" in names
    assert "PostgreSQL" in names
    assert "REST APIs" in names


def test_does_not_match_java_inside_javascript() -> None:
    names = {skill.name for skill in extract_skills("Primary language: JavaScript")}
    assert "JavaScript" in names
    assert "Java" not in names


def test_compare_skills_finds_missing_job_requirements() -> None:
    resume = extract_skills("React TypeScript PostgreSQL")
    job = extract_skills("React TypeScript Docker Kubernetes")
    matched, missing = compare_skills(resume, job)
    assert {skill.name for skill in matched} == {"React", "TypeScript"}
    assert {skill.name for skill in missing} == {"Docker", "Kubernetes"}
