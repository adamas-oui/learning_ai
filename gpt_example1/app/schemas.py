from pydantic import BaseModel, Field


class JobDescriptionRequest(BaseModel):
    job_description: str


class JobAnalysisResponse(BaseModel):
    summary: str
    match_score: int = Field(ge=0, le=100)
    strengths: list[str]
    gaps: list[str]
    recommendation: str
