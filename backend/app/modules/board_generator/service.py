"""
Board Generator Agent - core logic.

Responsibility: propose an initial visual layout for the mood board canvas.

PRECONDITION:  direction JSON is valid, image list non-empty
POSTCONDITION: none required - pure function, no DB writes here

Testable standalone: fake direction JSON + a hardcoded list of 3 fake
image IDs/urls. No real board/project needed to test this.
"""
import json
from google import genai
from app.core.config import settings
from .schemas import BoardGeneratorInput, BoardGeneratorOutput

_client = None

def _get_client():
    global _client
    if _client is None:
        if not settings.AI_API_KEY:
            raise RuntimeError("AI_API_KEY missing - check your .env file")
        _client = genai.Client(api_key=settings.AI_API_KEY)
    return _client


PROMPT_TEMPLATE = """You are laying out a mood board canvas. Given this
creative direction and this list of images, propose a layout. The canvas
is 1200 wide x 800 tall. Mix image tiles with a couple of color swatch
tiles (using palette colors) and one text tile showing the direction_name.
Avoid overlaps. Respond with ONLY valid JSON, no markdown fences, no
extra text, matching exactly this shape:

{{
  "elements": [
    {{"type": "image", "ref": "<image_id from the list>", "x": 0, "y": 0, "w": 300, "h": 300}},
    {{"type": "swatch", "color": "#HEXVAL", "x": 0, "y": 0, "w": 100, "h": 100}},
    {{"type": "text", "content": "short text", "x": 0, "y": 0, "w": 300, "h": 60}}
  ]
}}

Creative direction:
{direction_json}

Available images (use these ids as "ref" for image elements):
{image_ids_json}
"""


def run(data: BoardGeneratorInput) -> BoardGeneratorOutput:
    if not data.image_ids:
        raise ValueError("at least 1 image id is required")

    client = _get_client()
    prompt = PROMPT_TEMPLATE.format(
        direction_json=json.dumps(data.direction.model_dump(), indent=2),
        image_ids_json=json.dumps(data.image_ids),
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

    return BoardGeneratorOutput(**parsed)