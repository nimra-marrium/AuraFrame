"""
Board Generator Agent - HTTP interface. Stays THIN - delegates to service.py.
"""
from fastapi import APIRouter, HTTPException
from .schemas import BoardGeneratorAgentInput, BoardGeneratorAgentOutput
from . import service

router = APIRouter()


@router.post("/", response_model=BoardGeneratorAgentOutput)
def handle_board_generator(payload: BoardGeneratorAgentInput):
    try:
        return service.run(payload)
    except NotImplementedError:
        raise HTTPException(status_code=501, detail="Board Generator Agent not implemented yet")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
