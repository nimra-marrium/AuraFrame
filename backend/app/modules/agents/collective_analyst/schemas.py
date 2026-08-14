"""
Collective Analyst Agent - data contracts.

INPUT:  array of Visual Analyst JSON outputs
OUTPUT: JSON {recurring_colors[], recurring_motifs[], common_aesthetic, outliers[], overall_mood}
"""
from pydantic import BaseModel
from typing import List, Optional


class CollectiveAnalystAgentInput(BaseModel):
    # TODO: replace with real fields matching: array of Visual Analyst JSON outputs
    placeholder: Optional[str] = None


class CollectiveAnalystAgentOutput(BaseModel):
    # TODO: replace with real fields matching: JSON {recurring_colors[], recurring_motifs[], common_aesthetic, outliers[], overall_mood}
    placeholder: Optional[str] = None
