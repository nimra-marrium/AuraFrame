"""
Project module - HTTP interface. Thin: only translates HTTP <-> service.py.
"""

from fastapi import APIRouter, HTTPException, Header

from .schemas import ProjectCreateInput, ProjectOutput
from . import service
from app.core.database import get_supabase

router = APIRouter()


@router.post("/", response_model=ProjectOutput)
def create_project(
    payload: ProjectCreateInput,
    authorization: str = Header(...)
):
    try:
        if not authorization.startswith("Bearer "):
            raise HTTPException(
                status_code=401,
                detail="Authorization header must use Bearer token"
            )

        access_token = authorization.replace("Bearer ", "", 1)

        supabase = get_supabase()
        supabase.postgrest.auth(access_token)

        return service.create(payload)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{project_id}", response_model=ProjectOutput)
def get_project(project_id: str):

    try:
        return service.get(project_id)

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/user/{user_id}", response_model=list[ProjectOutput])
def list_projects(user_id: str):

    return service.list_for_user(user_id)