"""
Creative Director Agent - HTTP interface. Stays THIN - delegates to service.py.
"""
from fastapi import APIRouter, HTTPException
from .schemas import CreativeDirectorAgentInput, CreativeDirectorAgentOutput
from . import service

router = APIRouter()


@router.post("/", response_model=CreativeDirectorAgentOutput)
def handle_creative_director(payload: CreativeDirectorAgentInput):
    try:
        return service.run(payload)
    except NotImplementedError:
        raise HTTPException(status_code=501, detail="Creative Director Agent not implemented yet")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
