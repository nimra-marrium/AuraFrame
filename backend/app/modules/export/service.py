"""
Export - core logic.

Responsibility: Turn a saved board into a downloadable file.

PRECONDITION:  board/layout exists and is well-formed
POSTCONDITION: file generated and returned
"""
from .schemas import ExportInput, ExportOutput


def run(data: ExportInput) -> ExportOutput:
    """
    TODO: implement.
    This will read/write the database via the DB client.
    """
    raise NotImplementedError("Export not implemented yet - this is a skeleton")
