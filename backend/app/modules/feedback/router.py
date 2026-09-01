"""
Feedback module - HTTP interface.

Uses the requesting user's access_token so RLS can verify they own the
project this feedback belongs to.
"""
from fastapi import APIRouter, HTTPException, Header
from .schemas import FeedbackInput, FeedbackOutput
from . import service
from app.core.database import get_supabase


def _authenticate(authorization: str):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header must use Bearer token")
    access_token = authorization.replace("Bearer ", "", 1)
    supabase = get_supabase()
    supabase.postgrest.auth(access_token)


router = APIRouter()


@router.post("/", response_model=FeedbackOutput)
def create_feedback(payload: FeedbackInput, authorization: str = Header(...)):
    try:
        _authenticate(authorization)
        return service.create(payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/project/{project_id}", response_model=list[FeedbackOutput])
def list_feedback(project_id: str, authorization: str = Header(...)):
    _authenticate(authorization)
    return service.list_for_project(project_id)