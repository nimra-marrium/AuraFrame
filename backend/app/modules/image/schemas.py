"""
Image Upload module - data contracts.

INPUT:  project_id + image file (multipart, not JSON - see router.py)
OUTPUT: Image record with image_id + public url
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ImageOutput(BaseModel):
    id: str
    project_id: str
    url: str
    analysis: Optional[dict] = None
    created_at: datetime