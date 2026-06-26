from app.config import Settings
from app.models import AnalysisResponse
from app.providers import ExtractionProvider
from app.providers.heuristic import HeuristicExtractionProvider
from app.providers.openai_provider import OpenAIExtractionProvider
from app.scoring import score_extraction


def build_provider(settings: Settings) -> ExtractionProvider:
    if settings.analyzer_provider == "openai":
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required when ANALYZER_PROVIDER=openai")
        return OpenAIExtractionProvider(settings.openai_api_key, settings.openai_model)
    return HeuristicExtractionProvider()


class AnalyzerService:
    def __init__(self, provider: ExtractionProvider) -> None:
        self._provider = provider

    def analyze(self, resume_text: str, job_description: str) -> AnalysisResponse:
        extraction = self._provider.extract(resume_text, job_description)
        return score_extraction(extraction, provider=self._provider.name)

