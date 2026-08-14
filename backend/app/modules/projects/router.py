"""
Project - HTTP interface. Stays THIN - delegates to service.py.
"""
from fastapi import APIRouter, HTTPException
from .schemas import ProjectInput, ProjectOutput
from . import service

router = APIRouter()


@router.post("/", response_model=ProjectOutput)
def handle_projects(payload: ProjectInput):
    try:
        return service.run(payload)
    except NotImplementedError:
        raise HTTPException(status_code=501, detail="Project not implemented yet")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
