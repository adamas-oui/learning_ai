from typing import Protocol

from app.models import ExtractionBundle


class ExtractionProvider(Protocol):
    name: str

    def extract(self, resume_text: str, job_description: str) -> ExtractionBundle: ...

