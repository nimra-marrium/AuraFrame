"""
Project module - core logic.

Responsibility: create/read a project and its creative brief.

PRECONDITION:  valid user_id exists
POSTCONDITION: a Project row saved in DB

Testable standalone: call create()/get() with a fake user_id directly -
no HTTP layer needed, just a real Supabase connection.
"""
from app.core.database import get_supabase
from .schemas import ProjectCreateInput, ProjectOutput


def create(data: ProjectCreateInput) -> ProjectOutput:
    supabase = get_supabase()

    result = supabase.table("projects").insert({
        "user_id": data.user_id,
        "name": data.name,
        "brief_text": data.brief_text,
        "project_type": data.project_type,
        "target_audience": data.target_audience,
        "desired_mood": data.desired_mood,
    }).execute()

    if not result.data:
        raise ValueError("failed to create project")

    return ProjectOutput(**result.data[0])


def get(project_id: str) -> ProjectOutput:
    supabase = get_supabase()

    result = supabase.table("projects").select("*").eq("id", project_id).execute()

    if not result.data:
        raise ValueError(f"project {project_id} not found")

    return ProjectOutput(**result.data[0])


def list_for_user(user_id: str) -> list[ProjectOutput]:
    supabase = get_supabase()

    result = supabase.table("projects").select("*").eq("user_id", user_id).order(
        "created_at", desc=True
    ).execute()

    return [ProjectOutput(**row) for row in result.data]