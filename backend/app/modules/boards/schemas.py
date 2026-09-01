"""
Board module - data contracts.

INPUT:  project_id + layout JSON (elements array, same shape Board
        Generator Agent outputs)
OUTPUT: saved Board record
"""
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class BoardElement(BaseModel):
    type: str
    ref: Optional[str] = None
    color: Optional[str] = None
    content: Optional[str] = None
    x: float
    y: float
    w: float
    h: float


class BoardSaveInput(BaseModel):
    elements: List[BoardElement]


class BoardOutput(BaseModel):
    id: str
    project_id: str
    layout_data: List[BoardElement]
    updated_at: datetime