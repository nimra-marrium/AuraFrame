"""
Collective Analyst Agent - HTTP interface. Stays THIN - delegates to service.py.
"""
from fastapi import APIRouter, HTTPException
from .schemas import CollectiveAnalystAgentInput, CollectiveAnalystAgentOutput
from . import service

router = APIRouter()


@router.post("/", response_model=CollectiveAnalystAgentOutput)
def handle_collective_analyst(payload: CollectiveAnalystAgentInput):
    try:
        return service.run(payload)
    except NotImplementedError:
        raise HTTPException(status_code=501, detail="Collective Analyst Agent not implemented yet")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
