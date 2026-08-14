"""
Brief Analyst Agent - HTTP interface. Stays THIN - delegates to service.py.
"""
from fastapi import APIRouter, HTTPException
from .schemas import BriefAnalystAgentInput, BriefAnalystAgentOutput
from . import service

router = APIRouter()


@router.post("/", response_model=BriefAnalystAgentOutput)
def handle_brief_analyst(payload: BriefAnalystAgentInput):
    try:
        return service.run(payload)
    except NotImplementedError:
        raise HTTPException(status_code=501, detail="Brief Analyst Agent not implemented yet")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
