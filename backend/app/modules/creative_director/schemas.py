"""
Creative Director Agent - data contracts.

INPUT:  Brief Analyst output + Collective Analyst output
OUTPUT: JSON {direction_name, palette[], typography{heading,body}, imagery_direction, avoid[]}
"""
from pydantic import BaseModel
from typing import List, Optional
from app.modules.brief_analyst.schemas import BriefAnalystOutput
from app.modules.collective_analyst.schemas import CollectiveAnalystOutput


class CreativeDirectorInput(BaseModel):
    brief_analysis: BriefAnalystOutput
    collective_analysis: CollectiveAnalystOutput


class Typography(BaseModel):
    heading: Optional[str] = None
    body: Optional[str] = None


class CreativeDirectorOutput(BaseModel):
    direction_name: Optional[str] = None
    palette: List[str] = []
    typography: Optional[Typography] = None
    imagery_direction: Optional[str] = None
    avoid: List[str] = []