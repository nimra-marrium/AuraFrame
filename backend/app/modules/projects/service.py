"""
Project - core logic.

Responsibility: Create/read/update a project and its creative brief.

PRECONDITION:  valid user_id exists
POSTCONDITION: a Project row saved in DB
"""
from .schemas import ProjectInput, ProjectOutput


def run(data: ProjectInput) -> ProjectOutput:
    """
    TODO: implement.
    This will read/write the database via the DB client.
    """
    raise NotImplementedError("Project not implemented yet - this is a skeleton")
