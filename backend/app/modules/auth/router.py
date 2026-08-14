"""
Auth - HTTP interface. Stays THIN - delegates to service.py.
"""
from fastapi import APIRouter, HTTPException
from .schemas import AuthInput, AuthOutput
from . import service

router = APIRouter()


@router.post("/", response_model=AuthOutput)
def handle_auth(payload: AuthInput):
    try:
        return service.run(payload)
    except NotImplementedError:
        raise HTTPException(status_code=501, detail="Auth not implemented yet")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
