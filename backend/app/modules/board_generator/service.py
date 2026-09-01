"""
Board Generator Agent - core logic.
"""
import json
from google import genai
from app.core.config import settings
from app.core.logging import get_logger
from .schemas import BoardGeneratorInput, BoardGeneratorOutput

logger = get_logger(__name__)
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

    try:
        client = _get_client()
        prompt = PROMPT_TEMPLATE.format(
            direction_json=json.dumps(data.direction.model_dump(), indent=2),
            image_ids_json=json.dumps(data.image_ids),
        )

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt,
        )

        raw_text = response.text.strip()
        if raw_text.startswith("```"):
            raw_text = raw_text.strip("`")
            raw_text = raw_text.replace("json", "", 1).strip()

        parsed = json.loads(raw_text)
    except json.JSONDecodeError as e:
        logger.error(f"Board Generator returned non-JSON: {e}")
        raise ValueError("AI returned non-JSON response")
    except Exception as e:
        logger.error(f"Board Generator call failed: {e}")
        raise ValueError(f"board generation failed: {e}")

    logger.info(f"Board layout generated with {len(parsed.get('elements', []))} elements")
    return BoardGeneratorOutput(**parsed)