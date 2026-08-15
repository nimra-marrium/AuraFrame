"""
Collective Analyst Agent - HTTP interface.
Thin: only translates HTTP <-> service.py.
"""

from fastapi import APIRouter, HTTPException
from .schemas import CollectiveAnalystInput, CollectiveAnalystOutput
from . import service


router = APIRouter()


@router.post("/", response_model=CollectiveAnalystOutput)
def analyze_collective(payload: CollectiveAnalystInput):
    try:
        return service.run(payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))