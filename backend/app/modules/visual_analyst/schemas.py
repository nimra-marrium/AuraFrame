"""
Visual Analyst Agent - data contracts.

INPUT:  an image URL
OUTPUT: JSON {colors[], style, objects[], composition, lighting, keywords[]}
"""
from pydantic import BaseModel
from typing import List, Optional


class VisualAnalystInput(BaseModel):
    image_url: str


class VisualAnalystOutput(BaseModel):
    colors: List[str] = []          # hex codes, e.g. "#E8DFC8"
    style: Optional[str] = None
    objects: List[str] = []
    composition: Optional[str] = None
    lighting: Optional[str] = None
    keywords: List[str] = []