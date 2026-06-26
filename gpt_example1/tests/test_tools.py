from app.tools import estimate_skill_gap


def test_estimate_skill_gap_returns_matched_and_missing_skills() -> None:
    result = estimate_skill_gap(["Python", "FastAPI", "AWS"])

    assert result == {
        "matched_skills": ["python", "fastapi"],
        "missing_skills": ["aws"],
        "match_score": 67,
    }


def test_estimate_skill_gap_handles_empty_required_skills() -> None:
    result = estimate_skill_gap([])

    assert result == {
        "matched_skills": [],
        "missing_skills": [],
        "match_score": 0,
    }
