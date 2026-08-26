"""
Project module - data contracts.

INPUT (create):  user_id, name, brief_text, optional metadata
OUTPUT:          Project record with project_id
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProjectCreateInput(BaseModel):
    user_id: str
    name: str
    brief_text: str
    project_type: Optional[str] = None
    target_audience: Optional[str] = None
    desired_mood: Optional[str] = None


class ProjectOutput(BaseModel):
    id: str
    user_id: str
    name: str
    brief_text: str
    project_type: Optional[str] = None
    target_audience: Optional[str] = None
    desired_mood: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime