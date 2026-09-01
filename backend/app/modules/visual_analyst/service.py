"""
Visual Analyst Agent - core logic.
"""
import json
import httpx
from google import genai
from google.genai import types
from app.core.config import settings
from app.core.logging import get_logger
from .schemas import VisualAnalystInput, VisualAnalystOutput

logger = get_logger(__name__)
_client = None

def _get_client():
    global _client
    if _client is None:
        if not settings.AI_API_KEY:
            raise RuntimeError("AI_API_KEY missing - check your .env file")
        _client = genai.Client(api_key=settings.AI_API_KEY)
    return _client


PROMPT = """You are a visual analyst for a creative studio. Look at this
image and extract structured information. Respond with ONLY valid JSON,
no markdown fences, no extra text, matching exactly this shape:

{
  "colors": ["3-6 dominant hex color codes like #E8DFC8"],
  "style": "one short phrase describing the visual style",
  "objects": ["3-6 main objects/subjects visible"],
  "composition": "one short phrase describing framing/layout",
  "lighting": "one short phrase describing the lighting",
  "keywords": ["5-8 short descriptive keywords"]
}
"""


def run(data: VisualAnalystInput) -> VisualAnalystOutput:
    if not data.image_url.strip():
        raise ValueError("image_url cannot be empty")

    try:
        img_response = httpx.get(data.image_url, timeout=10, follow_redirects=True)
        img_response.raise_for_status()
    except httpx.HTTPError as e:
        logger.error(f"Could not fetch image {data.image_url}: {e}")
        raise ValueError("could not fetch image from image_url")

    content_type = img_response.headers.get("content-type", "image/jpeg")
    if not content_type.startswith("image/"):
        raise ValueError("image_url did not return an image")

    try:
        client = _get_client()
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=[
                types.Part.from_bytes(data=img_response.content, mime_type=content_type),
                PROMPT,
            ],
        )

        raw_text = response.text.strip()
        if raw_text.startswith("```"):
            raw_text = raw_text.strip("`")
            raw_text = raw_text.replace("json", "", 1).strip()

        parsed = json.loads(raw_text)
    except json.JSONDecodeError as e:
        logger.error(f"Visual Analyst returned non-JSON: {e}")
        raise ValueError("AI returned non-JSON response")
    except Exception as e:
        logger.error(f"Visual Analyst call failed for {data.image_url}: {e}")
        raise ValueError(f"visual analysis failed: {e}")

    logger.info(f"Image analyzed successfully: {data.image_url}")
    return VisualAnalystOutput(**parsed)