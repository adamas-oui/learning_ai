from fastapi import FastAPI

from app.schemas import JobAnalysisResponse, JobDescriptionRequest

app = FastAPI()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/analyze-job", response_model=JobAnalysisResponse)
def analyze_job(request: JobDescriptionRequest) -> JobAnalysisResponse:
    return JobAnalysisResponse(
        summary="This is a placeholder analysis for the submitted job description.",
        match_score=82,
        strengths=[
            "Relevant technical experience",
            "Clear communication skills",
            "Strong problem-solving background",
        ],
        gaps=[
            "More domain-specific experience may be helpful",
            "Leadership expectations should be clarified",
        ],
        recommendation="Proceed with a deeper resume-to-job comparison once LLM logic is added.",
    )
