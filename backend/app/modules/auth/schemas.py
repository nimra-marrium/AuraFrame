"""
Auth module - data contracts.

INPUT (signup/login): email + password
OUTPUT (on success): access_token + user_id + email
"""
from pydantic import BaseModel, EmailStr, Field


class SignupInput(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, description="Minimum 8 characters")


class LoginInput(BaseModel):
    email: EmailStr
    password: str


class AuthOutput(BaseModel):
    user_id: str
    email: str
    access_token: str