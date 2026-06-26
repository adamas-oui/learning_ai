import os

from openai import OpenAI

from app.schemas import JobAnalysisResponse

SYSTEM_PROMPT = """
You analyze job descriptions for a candidate.

Return a concise analysis with:
- summary: one short paragraph about the role
- match_score: an integer from 0 to 100
- strengths: a short list of likely candidate strengths
- gaps: a short list of likely skill or experience gaps
- recommendation: one practical next step
""".strip()


def analyze_job_description(job_description: str) -> JobAnalysisResponse:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

    response = client.responses.parse(
        model=model,
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"<job_description>\n{job_description}\n</job_description>",
            },
        ],
        text_format=JobAnalysisResponse,
    )

    if response.output_parsed is None:
        raise RuntimeError("The model did not return a valid job analysis")

    return response.output_parsed
