"""
Brief Analyst Agent - data contracts.

INPUT:  brief text (plain string)
OUTPUT: JSON {objective, audience, tone[], keywords[], constraints[]}
"""
from pydantic import BaseModel
from typing import List, Optional


class BriefAnalystAgentInput(BaseModel):
    # TODO: replace with real fields matching: brief text (plain string)
    placeholder: Optional[str] = None


class BriefAnalystAgentOutput(BaseModel):
    # TODO: replace with real fields matching: JSON {objective, audience, tone[], keywords[], constraints[]}
    placeholder: Optional[str] = None
