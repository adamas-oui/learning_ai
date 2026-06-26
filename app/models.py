from enum import Enum

from pydantic import BaseModel, Field, field_validator


class Importance(str, Enum):
    REQUIRED = "required"
    PREFERRED = "preferred"


class AnalysisRequest(BaseModel):
    resume_text: str = Field(min_length=20, max_length=50_000)
    job_description: str = Field(min_length=20, max_length=50_000)

    @field_validator("resume_text", "job_description")
    @classmethod
    def reject_blank_text(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("text cannot be blank")
        return value.strip()


class SkillEvidence(BaseModel):
    skill: str
    evidence: str


class JobRequirement(BaseModel):
    skill: str
    importance: Importance
    evidence: str


class ExtractionBundle(BaseModel):
    candidate_skills: list[SkillEvidence]
    job_requirements: list[JobRequirement]


class SkillMatch(BaseModel):
    skill: str
    importance: Importance
    resume_evidence: str
    job_evidence: str


class SkillGap(BaseModel):
    skill: str
    importance: Importance
    job_evidence: str


class AnalysisResponse(BaseModel):
    match_score: int = Field(ge=0, le=100)
    matched_skills: list[SkillMatch]
    missing_skills: list[SkillGap]
    summary: str
    provider: str
