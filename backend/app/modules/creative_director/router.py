"""
Creative Director Agent - HTTP interface. Thin: only translates HTTP <-> service.py.
"""
from fastapi import APIRouter, HTTPException
from .schemas import CreativeDirectorInput, CreativeDirectorOutput
from . import service
router = APIRouter()



@router.post("/", response_model=CreativeDirectorOutput)
def generate_direction(payload: CreativeDirectorInput):
    try:
        return service.run(payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))