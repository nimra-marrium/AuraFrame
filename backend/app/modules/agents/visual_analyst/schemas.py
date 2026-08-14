"""
Visual Analyst Agent - data contracts.

INPUT:  an image URL
OUTPUT: JSON {colors[], style, objects[], composition, lighting, keywords[]}
"""
from pydantic import BaseModel
from typing import List, Optional


class VisualAnalystAgentInput(BaseModel):
    # TODO: replace with real fields matching: an image URL
    placeholder: Optional[str] = None


class VisualAnalystAgentOutput(BaseModel):
    # TODO: replace with real fields matching: JSON {colors[], style, objects[], composition, lighting, keywords[]}
    placeholder: Optional[str] = None
