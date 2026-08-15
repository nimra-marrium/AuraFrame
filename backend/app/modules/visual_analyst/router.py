"""
Visual Analyst Agent - HTTP interface. Thin: only translates HTTP <-> service.py.
"""
from fastapi import APIRouter, HTTPException
from .schemas import VisualAnalystInput, VisualAnalystOutput
from . import service

router = APIRouter()


@router.post("/", response_model=VisualAnalystOutput)
def analyze_image(payload: VisualAnalystInput):
    try:
        return service.run(payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))