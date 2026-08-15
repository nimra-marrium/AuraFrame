"""
Collective Analyst Agent - data contracts.

INPUT:  array of Visual Analyst outputs (at least 2)
OUTPUT: JSON {recurring_colors[], recurring_motifs[], common_aesthetic, outliers[], overall_mood}
"""
from pydantic import BaseModel
from typing import List, Optional
from app.modules.visual_analyst.schemas import VisualAnalystOutput


class CollectiveAnalystInput(BaseModel):
    analyses: List[VisualAnalystOutput]


class CollectiveAnalystOutput(BaseModel):
    recurring_colors: List[str] = []
    recurring_motifs: List[str] = []
    common_aesthetic: Optional[str] = None
    outliers: List[str] = []
    overall_mood: Optional[str] = None