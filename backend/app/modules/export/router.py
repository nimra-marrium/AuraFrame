"""
Export - HTTP interface. Stays THIN - delegates to service.py.
"""
from fastapi import APIRouter, HTTPException
from .schemas import ExportInput, ExportOutput
from . import service

router = APIRouter()


@router.post("/", response_model=ExportOutput)
def handle_export(payload: ExportInput):
    try:
        return service.run(payload)
    except NotImplementedError:
        raise HTTPException(status_code=501, detail="Export not implemented yet")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
