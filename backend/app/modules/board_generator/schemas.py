"""
Board Generator Agent - data contracts.

INPUT:  Creative Direction output + list of image ids
OUTPUT: JSON {elements: [{type, ref/color/content, x, y, w, h}, ...]}
"""
from pydantic import BaseModel
from typing import List, Optional
from app.modules.creative_director.schemas import CreativeDirectorOutput


class BoardGeneratorInput(BaseModel):
    direction: CreativeDirectorOutput
    image_ids: List[str]


class BoardElement(BaseModel):
    type: str                       # "image" | "swatch" | "text"
    ref: Optional[str] = None       # image id, used when type == "image"
    color: Optional[str] = None     # hex, used when type == "swatch"
    content: Optional[str] = None   # text, used when type == "text"
    x: float
    y: float
    w: float
    h: float


class BoardGeneratorOutput(BaseModel):
    elements: List[BoardElement] = []