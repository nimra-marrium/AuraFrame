"""
Feedback/Eval - core logic.

Responsibility: Capture thumbs up/down on any AI output.

PRECONDITION:  valid project_id
POSTCONDITION: row saved, retrievable later
"""
from .schemas import FeedbackEvalInput, FeedbackEvalOutput


def run(data: FeedbackEvalInput) -> FeedbackEvalOutput:
    """
    TODO: implement.
    This will read/write the database via the DB client.
    """
    raise NotImplementedError("Feedback/Eval not implemented yet - this is a skeleton")
