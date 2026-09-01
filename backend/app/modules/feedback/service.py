"""
Feedback module - core logic.

Responsibility: capture thumbs up/down on any AI output.

PRECONDITION:  valid project_id
POSTCONDITION: row saved, retrievable later

Testable standalone: POST a fake rating directly - totally standalone,
doesn't touch AI or any other module.
"""
from app.core.database import get_supabase
from .schemas import FeedbackInput, FeedbackOutput

VALID_RATINGS = {"up", "down"}


def create(data: FeedbackInput) -> FeedbackOutput:
    if data.rating not in VALID_RATINGS:
        raise ValueError(f"rating must be one of {VALID_RATINGS}")

    supabase = get_supabase()

    result = supabase.table("feedback").insert({
        "project_id": data.project_id,
        "output_type": data.output_type,
        "rating": data.rating,
        "comment": data.comment,
    }).execute()

    if not result.data:
        raise ValueError("failed to save feedback")

    return FeedbackOutput(**result.data[0])


def list_for_project(project_id: str) -> list[FeedbackOutput]:
    supabase = get_supabase()
    result = supabase.table("feedback").select("*").eq("project_id", project_id).execute()
    return [FeedbackOutput(**row) for row in result.data]