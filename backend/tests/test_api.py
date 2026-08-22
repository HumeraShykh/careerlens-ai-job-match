from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)
SAMPLES = Path(__file__).resolve().parents[2] / "samples"


def test_health_endpoint() -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] in {"ok", "degraded"}
    assert "database" in body


def test_analyze_rejects_short_job_description() -> None:
    response = client.post(
        "/api/analyze",
        data={"resume_text": "Experienced software engineer using React and TypeScript daily.", "job_description": "hi"},
    )
    assert response.status_code == 400
    assert response.json()["detail"]["code"] == "job_too_short"


def test_analyze_sample_documents() -> None:
    resume = (SAMPLES / "sample-resume.txt").read_text(encoding="utf-8")
    job = (SAMPLES / "sample-job-description.txt").read_text(encoding="utf-8")
    response = client.post("/api/analyze", data={"resume_text": resume, "job_description": job})
    assert response.status_code == 200
    body = response.json()
    assert 0 <= body["breakdown"]["overall"] <= 100
    matched_names = {item["name"] for item in body["matched_skills"]}
    assert "Python" in matched_names
    assert "FastAPI" in matched_names
    assert body["suggestions"]
    assert "ATS" in body["disclaimer"] or "ats" in body["disclaimer"].lower()


def test_parse_txt_resume() -> None:
    content = (SAMPLES / "sample-resume.txt").read_bytes()
    response = client.post("/api/parse/resume", files={"file": ("sample-resume.txt", content, "text/plain")})
    assert response.status_code == 200
    assert response.json()["word_count"] > 50


def test_parse_rejects_png() -> None:
    response = client.post(
        "/api/parse/resume",
        files={"file": ("photo.png", b"not-an-image", "image/png")},
    )
    assert response.status_code == 400
    assert response.json()["detail"]["code"] == "unsupported_type"


def test_compare_ranks_sample_jobs() -> None:
    resume = (SAMPLES / "sample-resume.txt").read_text(encoding="utf-8")
    frontend = (SAMPLES / "sample-job-frontend.txt").read_text(encoding="utf-8")
    java = (SAMPLES / "sample-job-java.txt").read_text(encoding="utf-8")
    response = client.post(
        "/api/compare",
        data={
            "resume_text": resume,
            "job_description_1": frontend,
            "job_description_2": java,
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert len(body["jobs"]) == 2
    scores = {item["label"]: item["score"] for item in body["jobs"]}
    assert scores["Job 1"] > scores["Job 2"]
    assert body["jobs"][0]["is_best"] is True
    assert body["jobs"][0]["rank"] == 1
    assert body["winner_label"] == "Job 1"
    assert "better fit" in body["summary"].lower() or "very close" in body["summary"].lower()


def test_compare_includes_optional_third_job() -> None:
    resume = (SAMPLES / "sample-resume.txt").read_text(encoding="utf-8")
    ai = (SAMPLES / "sample-job-description.txt").read_text(encoding="utf-8")
    frontend = (SAMPLES / "sample-job-frontend.txt").read_text(encoding="utf-8")
    java = (SAMPLES / "sample-job-java.txt").read_text(encoding="utf-8")
    response = client.post(
        "/api/compare",
        data={
            "resume_text": resume,
            "job_description_1": ai,
            "job_description_2": frontend,
            "job_description_3": java,
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert len(body["jobs"]) == 3
    java_row = next(item for item in body["jobs"] if item["label"] == "Job 3")
    assert java_row["is_best"] is False
    assert java_row["score"] == min(item["score"] for item in body["jobs"])


def test_compare_rejects_short_second_job() -> None:
    resume = (SAMPLES / "sample-resume.txt").read_text(encoding="utf-8")
    job = (SAMPLES / "sample-job-description.txt").read_text(encoding="utf-8")
    response = client.post(
        "/api/compare",
        data={
            "resume_text": resume,
            "job_description_1": job,
            "job_description_2": "too short",
        },
    )
    assert response.status_code == 400
    assert response.json()["detail"]["code"] == "job_too_short"
