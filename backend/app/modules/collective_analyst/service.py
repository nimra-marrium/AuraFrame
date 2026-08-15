"""
Collective Analyst Agent - core logic.

Responsibility: find patterns ACROSS multiple images' analyses.

PRECONDITION:  array has at least 2 entries
POSTCONDITION: none required - pure function, no DB writes here

Testable standalone: hand-write 3-4 fake VisualAnalystOutput-shaped dicts
and feed them in directly - no real images or upload flow needed.
"""
import json
from google import genai
from app.core.config import settings
from .schemas import CollectiveAnalystInput, CollectiveAnalystOutput

_client = None

def _get_client():
    global _client
    if _client is None:
        if not settings.AI_API_KEY:
            raise RuntimeError("AI_API_KEY missing - check your .env file")
        _client = genai.Client(api_key=settings.AI_API_KEY)
    return _client


PROMPT_TEMPLATE = """You are a creative director reviewing a set of visual
reference analyses. Given these individual image analyses, find the
recurring patterns and outliers across ALL of them combined. Respond with
ONLY valid JSON, no markdown fences, no extra text, matching exactly:

{{
  "recurring_colors": ["3-6 hex colors that show up repeatedly across the set"],
  "recurring_motifs": ["3-6 repeated visual motifs/objects/themes"],
  "common_aesthetic": "one short phrase summarizing the shared aesthetic",
  "outliers": ["any images/elements that don't fit the pattern, or empty list"],
  "overall_mood": "one or two sentences describing the collective mood, written like: 'Your references consistently use...'"
}}

Individual image analyses:
{analyses_json}
"""


def run(data: CollectiveAnalystInput) -> CollectiveAnalystOutput:
    if len(data.analyses) < 2:
        raise ValueError("at least 2 image analyses are required")

    client = _get_client()
    analyses_json = json.dumps([a.model_dump() for a in data.analyses], indent=2)
    prompt = PROMPT_TEMPLATE.format(analyses_json=analyses_json)

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt,
    )

    raw_text = response.text.strip()
    if raw_text.startswith("```"):
        raw_text = raw_text.strip("`")
        raw_text = raw_text.replace("json", "", 1).strip()

    try:
        parsed = json.loads(raw_text)
    except json.JSONDecodeError:
        raise ValueError(f"AI returned non-JSON response: {raw_text[:200]}")

    return CollectiveAnalystOutput(**parsed)