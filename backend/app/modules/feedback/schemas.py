"""
Feedback/Eval - data contracts.

INPUT:  project_id, output_type, rating, optional comment
OUTPUT: saved Feedback record
"""
from pydantic import BaseModel
from typing import List, Optional


class FeedbackEvalInput(BaseModel):
    # TODO: replace with real fields matching: project_id, output_type, rating, optional comment
    placeholder: Optional[str] = None


class FeedbackEvalOutput(BaseModel):
    # TODO: replace with real fields matching: saved Feedback record
    placeholder: Optional[str] = None
