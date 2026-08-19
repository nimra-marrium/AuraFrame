"""
Creative Director Agent - core logic.

Responsibility: combine brief analysis + visual patterns into one
creative direction.

PRECONDITION:  both inputs non-null, matching expected shape
POSTCONDITION: none required - pure function, no DB writes here

Testable standalone: hand-write fake BriefAnalystOutput and
CollectiveAnalystOutput-shaped dicts and feed them in directly.
"""
import json
from google import genai
from app.core.config import settings
from .schemas import CreativeDirectorInput, CreativeDirectorOutput

_client = None

def _get_client():
    global _client
    if _client is None:
        if not settings.AI_API_KEY:
            raise RuntimeError("AI_API_KEY missing - check your .env file")
        _client = genai.Client(api_key=settings.AI_API_KEY)
    return _client


PROMPT_TEMPLATE = """You are a senior creative director. Combine this
brief analysis and this visual pattern analysis into ONE cohesive creative
direction. Respond with ONLY valid JSON, no markdown fences, no extra
text, matching exactly:

{{
  "direction_name": "a short evocative name for this creative direction, e.g. 'Soft Editorial Minimalism'",
  "palette": ["4-6 hex colors forming the final recommended palette"],
  "typography": {{"heading": "short font pairing suggestion for headings", "body": "short font pairing suggestion for body text"}},
  "imagery_direction": "1-2 sentences describing how imagery should be shot/selected",
  "avoid": ["2-4 things to explicitly avoid, to keep the direction consistent"]
}}

Brief analysis:
{brief_json}

Visual pattern analysis:
{collective_json}
"""


def run(data: CreativeDirectorInput) -> CreativeDirectorOutput:
    client = _get_client()
    prompt = PROMPT_TEMPLATE.format(
        brief_json=json.dumps(data.brief_analysis.model_dump(), indent=2),
        collective_json=json.dumps(data.collective_analysis.model_dump(), indent=2),
    )

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

    return CreativeDirectorOutput(**parsed)