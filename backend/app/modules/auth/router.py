"""
Auth module - HTTP interface. Thin: only translates HTTP <-> service.py.
"""
from fastapi import APIRouter, HTTPException
from .schemas import SignupInput, LoginInput, AuthOutput
from . import service

router = APIRouter()

@router.post("/signup", response_model=AuthOutput)
def signup(payload: SignupInput):
    try:
        return service.signup(payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=AuthOutput)
def login(payload: LoginInput):
    try:
        return service.login(payload)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))