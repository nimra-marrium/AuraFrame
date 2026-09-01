"""
Export module - core logic.
"""
from app.core.database import get_supabase
from app.core.logging import get_logger

logger = get_logger(__name__)


def export_project(project_id: str) -> dict:
    supabase = get_supabase()

    try:
        project_result = supabase.table("projects").select("*").eq("id", project_id).execute()
        if not project_result.data:
            raise ValueError(f"project {project_id} not found")
        project = project_result.data[0]

        board_result = supabase.table("boards").select("*").eq("project_id", project_id).execute()
        board = board_result.data[0] if board_result.data else None

        images_result = supabase.table("images").select("*").eq("project_id", project_id).execute()
        images = images_result.data
    except ValueError:
        raise
    except Exception as e:
        logger.error(f"Export failed for project {project_id}: {e}")
        raise ValueError(f"failed to export project: {e}")

    logger.info(f"Project exported: {project_id}")
    return {
        "project": {
            "name": project["name"],
            "brief_text": project["brief_text"],
            "project_type": project.get("project_type"),
            "target_audience": project.get("target_audience"),
        },
        "images": [{"url": img["url"], "analysis": img.get("analysis")} for img in images],
        "board_layout": board["layout_data"] if board else [],
        "exported_at": None,
    }