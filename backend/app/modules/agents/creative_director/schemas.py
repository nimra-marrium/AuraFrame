"""
Creative Director Agent - data contracts.

INPUT:  Brief Analyst output + Collective Analyst output
OUTPUT: JSON {direction_name, palette[], typography, imagery_direction, avoid[]}
"""
from pydantic import BaseModel
from typing import List, Optional


class CreativeDirectorAgentInput(BaseModel):
    # TODO: replace with real fields matching: Brief Analyst output + Collective Analyst output
    placeholder: Optional[str] = None


class CreativeDirectorAgentOutput(BaseModel):
    # TODO: replace with real fields matching: JSON {direction_name, palette[], typography, imagery_direction, avoid[]}
    placeholder: Optional[str] = None
