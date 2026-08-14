"""
Image Upload - data contracts.

INPUT:  project_id, image file
OUTPUT: Image record with image_id + public url
"""
from pydantic import BaseModel
from typing import List, Optional


class ImageUploadInput(BaseModel):
    # TODO: replace with real fields matching: project_id, image file
    placeholder: Optional[str] = None


class ImageUploadOutput(BaseModel):
    # TODO: replace with real fields matching: Image record with image_id + public url
    placeholder: Optional[str] = None
