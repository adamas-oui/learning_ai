from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    assert client.get("/health").json() == {"status": "ok"}


def test_analyze_with_offline_provider() -> None:
    response = client.post(
        "/analyze",
        json={
            "resume_text": "I built Python services on AWS and used PostgreSQL in production.",
            "job_description": (
                "We require Python and AWS experience. Kubernetes experience is a plus."
            ),
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["match_score"] == 80
    assert {item["skill"] for item in body["matched_skills"]} == {"Python", "AWS"}
    assert [item["skill"] for item in body["missing_skills"]] == ["Kubernetes"]

