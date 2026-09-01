"""
Export module - HTTP interface.
"""
import json
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Header, Response
from . import service
from app.core.database import get_supabase

router = APIRouter()


@router.get("/{project_id}")
def export_project(project_id: str, authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header must use Bearer token")
    access_token = authorization.replace("Bearer ", "", 1)
    get_supabase().postgrest.auth(access_token)

    try:
        data = service.export_project(project_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    data["exported_at"] = datetime.now(timezone.utc).isoformat()

    return Response(
        content=json.dumps(data, indent=2),
        media_type="application/json",
        headers={"Content-Disposition": f'attachment; filename="auraframe-export-{project_id}.json"'},
    )