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
from .schemas import BoardSaveInput, BoardOutput


def save(project_id: str, data: BoardSaveInput) -> BoardOutput:
    supabase = get_supabase()

    layout_json = [el.model_dump() for el in data.elements]

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

    if not result.data:
        raise ValueError("failed to save board")

    return BoardOutput(**result.data[0])


def get(project_id: str) -> BoardOutput:
    supabase = get_supabase()

    result = supabase.table("boards").select("*").eq("project_id", project_id).execute()

    if not result.data:
        raise ValueError(f"no board found for project {project_id}")

    return BoardOutput(**result.data[0])