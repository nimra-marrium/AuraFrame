"""
Feedback module - data contracts.

INPUT:  project_id, output_type, rating (up/down), optional comment
OUTPUT: saved Feedback record
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class FeedbackInput(BaseModel):
    project_id: str
    output_type: str   # "palette" | "direction" | "board" etc
    rating: str         # "up" | "down"
    comment: Optional[str] = None


class FeedbackOutput(BaseModel):
    id: str
    project_id: str
    output_type: str
    rating: str
    comment: Optional[str] = None
    created_at: datetime