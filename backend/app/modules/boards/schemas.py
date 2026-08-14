"""
Board - data contracts.

INPUT:  project_id + layout JSON
OUTPUT: saved Board record
"""
from pydantic import BaseModel
from typing import List, Optional


class BoardInput(BaseModel):
    # TODO: replace with real fields matching: project_id + layout JSON
    placeholder: Optional[str] = None


class BoardOutput(BaseModel):
    # TODO: replace with real fields matching: saved Board record
    placeholder: Optional[str] = None
