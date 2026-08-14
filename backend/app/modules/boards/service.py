"""
Board - core logic.

Responsibility: Persist and update the board layout as the user edits.

PRECONDITION:  valid project_id, layout JSON well-formed
POSTCONDITION: Board.layout_data updated in DB
"""
from .schemas import BoardInput, BoardOutput


def run(data: BoardInput) -> BoardOutput:
    """
    TODO: implement.
    This will read/write the database via the DB client.
    """
    raise NotImplementedError("Board not implemented yet - this is a skeleton")
