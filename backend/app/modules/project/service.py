"""
Project module - core logic.
"""
from app.core.database import get_supabase
from app.core.logging import get_logger
from .schemas import ProjectCreateInput, ProjectOutput

logger = get_logger(__name__)


def create(data: ProjectCreateInput) -> ProjectOutput:
    supabase = get_supabase()

    try:
        result = supabase.table("projects").insert({
            "user_id": data.user_id,
            "name": data.name,
            "brief_text": data.brief_text,
            "project_type": data.project_type,
            "target_audience": data.target_audience,
            "desired_mood": data.desired_mood,
        }).execute()
    except Exception as e:
        logger.error(f"Project creation failed for user {data.user_id}: {e}")
        raise ValueError(f"failed to create project: {e}")

    if not result.data:
        logger.error(f"Project insert returned no data for user {data.user_id}")
        raise ValueError("failed to create project")

    logger.info(f"Project created: {result.data[0]['id']}")
    return ProjectOutput(**result.data[0])


def get(project_id: str) -> ProjectOutput:
    supabase = get_supabase()
    try:
        result = supabase.table("projects").select("*").eq("id", project_id).execute()
    except Exception as e:
        logger.error(f"Project fetch failed for {project_id}: {e}")
        raise ValueError(f"failed to fetch project: {e}")

    if not result.data:
        raise ValueError(f"project {project_id} not found")

    return ProjectOutput(**result.data[0])


def list_for_user(user_id: str) -> list[ProjectOutput]:
    supabase = get_supabase()
    try:
        result = supabase.table("projects").select("*").eq("user_id", user_id).order(
            "created_at", desc=True
        ).execute()
    except Exception as e:
        logger.error(f"Project list failed for user {user_id}: {e}")
        raise ValueError(f"failed to list projects: {e}")

    return [ProjectOutput(**row) for row in result.data]