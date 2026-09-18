"""
Project module - HTTP interface. Thin: only translates HTTP <-> service.py.
"""

from fastapi import APIRouter, HTTPException, Header, Response

from .schemas import ProjectCreateInput, ProjectUpdateInput, ProjectOutput
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


@router.put("/{project_id}", response_model=ProjectOutput)
def update_project(
    project_id: str,
    payload: ProjectUpdateInput,
    authorization: str = Header(...),
):
    try:
        if not authorization.startswith("Bearer "):
            raise HTTPException(
                status_code=401,
                detail="Authorization header must use Bearer token",
            )

        access_token = authorization.replace("Bearer ", "", 1)
        supabase = get_supabase()
        supabase.postgrest.auth(access_token)

        return service.update(project_id, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/user/{user_id}", response_model=list[ProjectOutput])
def list_projects(user_id: str):

    return service.list_for_user(user_id)


@router.delete("/{project_id}", status_code=204)
def delete_project(
    project_id: str,
    authorization: str = Header(...),
):
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Authorization header must use Bearer token",
        )

    access_token = authorization.replace("Bearer ", "", 1)
    supabase = get_supabase()

    # Find out who is logged in, so users can only delete their own projects
    try:
        user_response = supabase.auth.get_user(access_token)
        user_id = user_response.user.id
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    supabase.postgrest.auth(access_token)

    try:
        service.delete(project_id, user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    return Response(status_code=204)
