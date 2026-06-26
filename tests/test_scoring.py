from app.models import ExtractionBundle, Importance, JobRequirement, SkillEvidence
from app.scoring import score_extraction


def test_required_skills_receive_more_weight() -> None:
    extraction = ExtractionBundle(
        candidate_skills=[SkillEvidence(skill="Python", evidence="Built APIs with Python.")],
        job_requirements=[
            JobRequirement(
                skill="Python",
                importance=Importance.REQUIRED,
                evidence="Python is required.",
            ),
            JobRequirement(
                skill="Kubernetes",
                importance=Importance.PREFERRED,
                evidence="Kubernetes is a plus.",
            ),
        ],
    )

    result = score_extraction(extraction, provider="test")

    assert result.match_score == 67
    assert [item.skill for item in result.matched_skills] == ["Python"]
    assert [item.skill for item in result.missing_skills] == ["Kubernetes"]


def test_no_requirements_produces_zero_score() -> None:
    result = score_extraction(
        ExtractionBundle(candidate_skills=[], job_requirements=[]), provider="test"
    )

    assert result.match_score == 0

