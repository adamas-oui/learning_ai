from functools import lru_cache

from fastapi import Depends, FastAPI

from app.config import get_settings
from app.models import AnalysisRequest, AnalysisResponse
from app.service import AnalyzerService, build_provider

app = FastAPI(title="AI Job Analyzer", version="0.1.0")


@lru_cache
def get_analyzer() -> AnalyzerService:
    return AnalyzerService(build_provider(get_settings()))


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/analyze", response_model=AnalysisResponse)
def analyze(
    request: AnalysisRequest,
    analyzer: AnalyzerService = Depends(get_analyzer),
) -> AnalysisResponse:
    return analyzer.analyze(request.resume_text, request.job_description)

