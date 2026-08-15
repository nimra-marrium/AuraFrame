"""
Brief Analyst Agent - core logic.

Responsibility: turn raw brief text into structured creative tags.

PRECONDITION:  brief_text is non-empty
POSTCONDITION: none required - pure function, no DB writes here

Testable standalone: call run() with any hardcoded string, no other
module, database, or HTTP layer needs to exist.
"""
import json
from google import genai
from app.core.config import settings
from .schemas import BriefAnalystInput, BriefAnalystOutput

_client = None

def _get_client():
    global _client
    if _client is None:
        if not settings.AI_API_KEY:
            raise RuntimeError("AI_API_KEY missing - check your .env file")
        _client = genai.Client(api_key=settings.AI_API_KEY)
    return _client


PROMPT_TEMPLATE = """You are a creative brief analyst. Given a raw creative
brief, extract structured information. Respond with ONLY valid JSON, no
markdown fences, no extra text, matching exactly this shape:

{{
  "objective": "one sentence describing the project goal",
  "audience": "one sentence describing the target audience",
  "tone": ["3-5 short tone words"],
  "keywords": ["5-8 short visual/creative keywords"],
  "constraints": ["any explicit constraints mentioned, or empty list"]
}}

Brief:
\"\"\"{brief_text}\"\"\"
"""


def run(data: BriefAnalystInput) -> BriefAnalystOutput:
    if not data.brief_text.strip():
        raise ValueError("brief_text cannot be empty")

    client = _get_client()
    prompt = PROMPT_TEMPLATE.format(brief_text=data.brief_text)

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
    )

    raw_text = response.text.strip()
    # Gemini sometimes wraps JSON in ```json fences despite instructions - strip if present
    if raw_text.startswith("```"):
        raw_text = raw_text.strip("`")
        raw_text = raw_text.replace("json", "", 1).strip()

    try:
        parsed = json.loads(raw_text)
    except json.JSONDecodeError:
        raise ValueError(f"AI returned non-JSON response: {raw_text[:200]}")

    return BriefAnalystOutput(**parsed)