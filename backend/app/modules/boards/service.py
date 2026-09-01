"""
Board module - core logic.

Responsibility: persist and update the board layout as the user edits.

PRECONDITION:  valid project_id, layout JSON well-formed
POSTCONDITION: Board.layout_data updated in DB

Testable standalone: PATCH a fake layout JSON directly - no canvas UI or
AI needed to test the save/load logic. One board per project (unique
constraint), so save() creates on first call, updates after that.
"""
from app.core.database import get_supabase
from app.core.logging import get_logger
from .schemas import BoardSaveInput, BoardOutput

logger = get_logger(__name__)


def save(project_id: str, data: BoardSaveInput) -> BoardOutput:
    supabase = get_supabase()
    layout_json = [el.model_dump() for el in data.elements]

    try:
        existing = supabase.table("boards").select("id").eq("project_id", project_id).execute()

        if existing.data:
            result = supabase.table("boards").update({
                "layout_data": layout_json,
            }).eq("project_id", project_id).execute()
        else:
            result = supabase.table("boards").insert({
                "project_id": project_id,
                "layout_data": layout_json,
            }).execute()
    except Exception as e:
        logger.error(f"Board save failed for project {project_id}: {e}")
        raise ValueError(f"failed to save board: {e}")

    if not result.data:
        logger.error(f"Board save returned no data for project {project_id}")
        raise ValueError("failed to save board")

    logger.info(f"Board saved for project {project_id}")
    return BoardOutput(**result.data[0])


def get(project_id: str) -> BoardOutput:
    supabase = get_supabase()

    try:
        result = supabase.table("boards").select("*").eq("project_id", project_id).execute()
    except Exception as e:
        logger.error(f"Board fetch failed for project {project_id}: {e}")
        raise ValueError(f"failed to fetch board: {e}")

    if not result.data:
        raise ValueError(f"no board found for project {project_id}")

    return BoardOutput(**result.data[0])