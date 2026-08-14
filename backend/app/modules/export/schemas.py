"""
Export - data contracts.

INPUT:  board_id or raw layout JSON
OUTPUT: PDF or PNG file
"""
from pydantic import BaseModel
from typing import List, Optional


class ExportInput(BaseModel):
    # TODO: replace with real fields matching: board_id or raw layout JSON
    placeholder: Optional[str] = None


class ExportOutput(BaseModel):
    # TODO: replace with real fields matching: PDF or PNG file
    placeholder: Optional[str] = None
