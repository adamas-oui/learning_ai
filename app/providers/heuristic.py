import re

from app.models import ExtractionBundle, Importance, JobRequirement, SkillEvidence

# Intentionally small: this is a baseline for comparing the LLM, not a complete ontology.
SKILLS = {
    "amazon web services": "AWS",
    "aws": "AWS",
    "c++": "C++",
    "docker": "Docker",
    "fastapi": "FastAPI",
    "git": "Git",
    "go": "Go",
    "java": "Java",
    "javascript": "JavaScript",
    "kubernetes": "Kubernetes",
    "machine learning": "Machine Learning",
    "postgresql": "PostgreSQL",
    "python": "Python",
    "react": "React",
    "redis": "Redis",
    "sql": "SQL",
    "typescript": "TypeScript",
}


def _contains(text: str, phrase: str) -> bool:
    return re.search(rf"(?<!\w){re.escape(phrase)}(?!\w)", text, re.IGNORECASE) is not None


def _sentence_with(text: str, phrase: str) -> str:
    sentences = re.split(r"(?<=[.!?])\s+|\n+", text)
    return next((part.strip() for part in sentences if _contains(part, phrase)), phrase)


class HeuristicExtractionProvider:
    name = "heuristic"

    def extract(self, resume_text: str, job_description: str) -> ExtractionBundle:
        candidate: dict[str, SkillEvidence] = {}
        requirements: dict[str, JobRequirement] = {}

        for phrase, canonical in SKILLS.items():
            if _contains(resume_text, phrase):
                candidate[canonical.casefold()] = SkillEvidence(
                    skill=canonical,
                    evidence=_sentence_with(resume_text, phrase),
                )
            if _contains(job_description, phrase):
                evidence = _sentence_with(job_description, phrase)
                preferred = re.search(
                    r"preferred|nice[- ]to[- ]have|bonus|a plus", evidence, re.IGNORECASE
                )
                requirements[canonical.casefold()] = JobRequirement(
                    skill=canonical,
                    importance=Importance.PREFERRED if preferred else Importance.REQUIRED,
                    evidence=evidence,
                )

        return ExtractionBundle(
            candidate_skills=list(candidate.values()),
            job_requirements=list(requirements.values()),
        )

