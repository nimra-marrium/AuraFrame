"""
Visual Analyst Agent - core logic.

Responsibility: analyze ONE image, return structured visual data.

PRECONDITION:  image_url is a reachable, valid image
POSTCONDITION: none required - pure function, no DB writes here

Testable standalone: call run() with any public image URL, no other
module, database, or upload flow needs to exist.
"""
import json
import httpx
from google import genai
from google.genai import types
from app.core.config import settings
from .schemas import VisualAnalystInput, VisualAnalystOutput

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

    # fetch the image bytes ourselves so we control errors clearly
    try:
        img_response = httpx.get(data.image_url, timeout=10, follow_redirects=True)
        img_response.raise_for_status()
    except httpx.HTTPError:
        raise ValueError(f"could not fetch image from image_url")

    content_type = img_response.headers.get("content-type", "image/jpeg")
    if not content_type.startswith("image/"):
        raise ValueError("image_url did not return an image")

    client = _get_client()
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=[
            types.Part.from_bytes(data=img_response.content, mime_type=content_type),
            PROMPT,
        ],
    )

    raw_text = response.text.strip()
    if raw_text.startswith("```"):
        raw_text = raw_text.strip("`")
        raw_text = raw_text.replace("json", "", 1).strip()

    try:
        parsed = json.loads(raw_text)
    except json.JSONDecodeError:
        raise ValueError(f"AI returned non-JSON response: {raw_text[:200]}")

    return VisualAnalystOutput(**parsed)