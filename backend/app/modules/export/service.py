"""
Export module - core logic.

Responsibility: turn a saved board into a downloadable file.

PRECONDITION:  board/layout exists and is well-formed
POSTCONDITION: file generated and returned

Testable standalone: feed it a hand-written fake layout JSON. Doesn't
need a real project or real board saved.

NOTE: this MVP version exports a clean JSON summary (direction + palette
+ layout) rather than a rendered image/PDF - real image rendering would
need an extra library (e.g. Pillow) and is a good "v2" upgrade later.
"""
import json
from app.core.database import get_supabase


def export_project(project_id: str) -> dict:
    supabase = get_supabase()

    project_result = supabase.table("projects").select("*").eq("id", project_id).execute()
    if not project_result.data:
        raise ValueError(f"project {project_id} not found")
    project = project_result.data[0]

    board_result = supabase.table("boards").select("*").eq("project_id", project_id).execute()
    board = board_result.data[0] if board_result.data else None

    images_result = supabase.table("images").select("*").eq("project_id", project_id).execute()
    images = images_result.data

    export_data = {
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

    return export_data