MY_SKILLS = [
    "python",
    "fastapi",
    "pydantic",
    "sql",
    "git",
]


def estimate_skill_gap(required_skills: list[str]) -> dict[str, object]:
    normalized_my_skills = {skill.lower() for skill in MY_SKILLS}
    normalized_required_skills = [skill.lower() for skill in required_skills]

    matched_skills = [
        skill
        for skill in normalized_required_skills
        if skill in normalized_my_skills
    ]
    missing_skills = [
        skill
        for skill in normalized_required_skills
        if skill not in normalized_my_skills
    ]
    match_score = (
        round(len(matched_skills) / len(normalized_required_skills) * 100)
        if normalized_required_skills
        else 0
    )

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "match_score": match_score,
    }
