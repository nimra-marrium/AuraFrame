"""
Visual Analyst Agent - HTTP interface. Stays THIN - delegates to service.py.
"""
from fastapi import APIRouter, HTTPException
from .schemas import VisualAnalystAgentInput, VisualAnalystAgentOutput
from . import service

router = APIRouter()


@router.post("/", response_model=VisualAnalystAgentOutput)
def handle_visual_analyst(payload: VisualAnalystAgentInput):
    try:
        return service.run(payload)
    except NotImplementedError:
        raise HTTPException(status_code=501, detail="Visual Analyst Agent not implemented yet")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
