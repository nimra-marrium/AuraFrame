"""
Board module - HTTP interface.

Uses the requesting user's access_token (not service_role) so RLS can
verify they actually own the project this board belongs to - same
pattern as project/router.py.
"""
from fastapi import APIRouter, HTTPException, Header
from .schemas import BoardSaveInput, BoardOutput
from . import service
from app.core.database import get_supabase


def _authenticate(authorization: str):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header must use Bearer token")
    access_token = authorization.replace("Bearer ", "", 1)
    supabase = get_supabase()
    supabase.postgrest.auth(access_token)


router = APIRouter()


@router.put("/{project_id}", response_model=BoardOutput)
def save_board(project_id: str, payload: BoardSaveInput, authorization: str = Header(...)):
    try:
        _authenticate(authorization)
        return service.save(project_id, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{project_id}", response_model=BoardOutput)
def get_board(project_id: str, authorization: str = Header(...)):
    try:
        _authenticate(authorization)
        return service.get(project_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))