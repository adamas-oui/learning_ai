from pydantic import BaseModel


class JobDescriptionRequest(BaseModel):
    job_description: str


class JobAnalysisResponse(BaseModel):
    summary: str
    match_score: int
    strengths: list[str]
    gaps: list[str]
    recommendation: str
