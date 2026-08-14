"""
Project - data contracts.

INPUT:  user_id, project name, brief text, mood tags
OUTPUT: Project record with project_id
"""
from pydantic import BaseModel
from typing import List, Optional


class ProjectInput(BaseModel):
    # TODO: replace with real fields matching: user_id, project name, brief text, mood tags
    placeholder: Optional[str] = None


class ProjectOutput(BaseModel):
    # TODO: replace with real fields matching: Project record with project_id
    placeholder: Optional[str] = None
