"""
Auth - data contracts.

INPUT:  email + password
OUTPUT: session token + user_id
"""
from pydantic import BaseModel
from typing import List, Optional


class AuthInput(BaseModel):
    # TODO: replace with real fields matching: email + password
    placeholder: Optional[str] = None


class AuthOutput(BaseModel):
    # TODO: replace with real fields matching: session token + user_id
    placeholder: Optional[str] = None
