from app.models import AnalysisResponse, ExtractionBundle, Importance, SkillGap, SkillMatch

WEIGHTS = {
    Importance.REQUIRED: 2,
    Importance.PREFERRED: 1,
}


def _normalize(skill: str) -> str:
    return " ".join(skill.casefold().split())


def score_extraction(extraction: ExtractionBundle, provider: str) -> AnalysisResponse:
    candidate_by_skill = {
        _normalize(item.skill): item for item in extraction.candidate_skills
    }
    matches: list[SkillMatch] = []
    gaps: list[SkillGap] = []
    earned_weight = 0
    possible_weight = 0

    for requirement in extraction.job_requirements:
        weight = WEIGHTS[requirement.importance]
        possible_weight += weight
        candidate = candidate_by_skill.get(_normalize(requirement.skill))
        if candidate:
            earned_weight += weight
            matches.append(
                SkillMatch(
                    skill=requirement.skill,
                    importance=requirement.importance,
                    resume_evidence=candidate.evidence,
                    job_evidence=requirement.evidence,
                )
            )
        else:
            gaps.append(
                SkillGap(
                    skill=requirement.skill,
                    importance=requirement.importance,
                    job_evidence=requirement.evidence,
                )
            )

    score = round(100 * earned_weight / possible_weight) if possible_weight else 0
    summary = (
        f"Matched {len(matches)} of {len(extraction.job_requirements)} extracted requirements; "
        f"{sum(g.importance == Importance.REQUIRED for g in gaps)} required gaps remain."
    )
    return AnalysisResponse(
        match_score=score,
        matched_skills=matches,
        missing_skills=gaps,
        summary=summary,
        provider=provider,
    )

