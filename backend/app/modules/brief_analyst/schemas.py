"""
Brief Analyst Agent - data contracts.

INPUT:  brief text (plain string)
OUTPUT: JSON {objective, audience, tone[], keywords[], constraints[]}
"""
from pydantic import BaseModel
from typing import List, Optional


class BriefAnalystInput(BaseModel):
    brief_text: str


class BriefAnalystOutput(BaseModel):
    objective: Optional[str] = None
    audience: Optional[str] = None
    tone: List[str] = []
    keywords: List[str] = []
    constraints: List[str] = []