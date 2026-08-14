"""
Auth - core logic.

Responsibility: Sign up, log in, log out, identify the requesting user.

PRECONDITION:  email is valid format, password meets min length
POSTCONDITION: a User row exists in DB; caller has a token
"""
from .schemas import AuthInput, AuthOutput


def run(data: AuthInput) -> AuthOutput:
    """
    TODO: implement.
    This will read/write the database via the DB client.
    """
    raise NotImplementedError("Auth not implemented yet - this is a skeleton")
