"""
Board Generator Agent - data contracts.

INPUT:  Creative Direction JSON + list of image records
OUTPUT: JSON array of layout elements [{type, ref, x, y, w, h}]
"""
from pydantic import BaseModel
from typing import List, Optional


class BoardGeneratorAgentInput(BaseModel):
    # TODO: replace with real fields matching: Creative Direction JSON + list of image records
    placeholder: Optional[str] = None


class BoardGeneratorAgentOutput(BaseModel):
    # TODO: replace with real fields matching: JSON array of layout elements [{type, ref, x, y, w, h}]
    placeholder: Optional[str] = None
