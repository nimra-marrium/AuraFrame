"""
Board - HTTP interface. Stays THIN - delegates to service.py.
"""
from fastapi import APIRouter, HTTPException
from .schemas import BoardInput, BoardOutput
from . import service

router = APIRouter()


@router.post("/", response_model=BoardOutput)
def handle_boards(payload: BoardInput):
    try:
        return service.run(payload)
    except NotImplementedError:
        raise HTTPException(status_code=501, detail="Board not implemented yet")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
