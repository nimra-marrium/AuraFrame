"""
Board Generator Agent - HTTP interface. Thin: only translates HTTP <-> service.py.
"""
from fastapi import APIRouter, HTTPException
from .schemas import BoardGeneratorInput, BoardGeneratorOutput
from . import service

router = APIRouter()


@router.post("/", response_model=BoardGeneratorOutput)
def generate_board(payload: BoardGeneratorInput):
    try:
        return service.run(payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))