from openai import OpenAI

from app.models import ExtractionBundle

SYSTEM_PROMPT = """
You extract factual hiring evidence from a resume and job description.

Rules:
- Return only skills explicitly supported by the supplied text.
- Keep each evidence field as a short, exact excerpt from its source.
- Normalize obvious aliases (for example, Postgres -> PostgreSQL), but do not infer skills.
- A job requirement is preferred only when the text clearly marks it as optional, preferred,
  a bonus, or nice-to-have. Otherwise classify it as required.
- Do not score the candidate and do not write recommendations.
""".strip()


class OpenAIExtractionProvider:
    name = "openai"

    def __init__(self, api_key: str, model: str) -> None:
        self._client = OpenAI(api_key=api_key)
        self._model = model

    def extract(self, resume_text: str, job_description: str) -> ExtractionBundle:
        response = self._client.responses.parse(
            model=self._model,
            input=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": (
                        f"<resume>\n{resume_text}\n</resume>\n\n"
                        f"<job_description>\n{job_description}\n</job_description>"
                    ),
                },
            ],
            text_format=ExtractionBundle,
        )
        if response.output_parsed is None:
            raise RuntimeError("The model did not return a parsed extraction")
        return response.output_parsed

