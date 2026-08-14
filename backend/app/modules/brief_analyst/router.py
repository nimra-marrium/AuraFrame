"""
Brief Analyst Agent - HTTP interface. Thin: only translates HTTP <-> service.py.
"""
from fastapi import APIRouter, HTTPException
from .schemas import BriefAnalystInput, BriefAnalystOutput
from . import service

router = APIRouter()


@router.post("/", response_model=BriefAnalystOutput)
def analyze_brief(payload: BriefAnalystInput):
    try:
        return service.run(payload)
    except NotImplementedError:
        raise HTTPException(status_code=501, detail="Brief Analyst not implemented yet")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))