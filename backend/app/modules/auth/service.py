"""
Auth module - core logic.

Responsibility: sign up, log in, identify the requesting user.

PRECONDITION:  email is valid format, password meets min length
               (both already enforced by schemas.py before this runs)
POSTCONDITION: on signup, a user exists in Supabase Auth
               on login, caller receives a valid access_token

This module is testable standalone: call signup()/login() directly with
a real (test) email/password, no other module needs to exist.
"""
from app.core.database import get_supabase
from .schemas import SignupInput, LoginInput, AuthOutput


def signup(data: SignupInput) -> AuthOutput:
    supabase = get_supabase()

    result = supabase.auth.sign_up({
        "email": data.email,
        "password": data.password,
    })

    if result.user is None:
        raise ValueError("Signup failed - email may already be registered")

    # Supabase requires email confirmation by default, so session may be None
    # right after signup. access_token will be empty until they confirm.
    token = result.session.access_token if result.session else ""

    return AuthOutput(
        user_id=result.user.id,
        email=result.user.email,
        access_token=token,
    )


def login(data: LoginInput) -> AuthOutput:
    supabase = get_supabase()

    try:
        result = supabase.auth.sign_in_with_password({
            "email": data.email,
            "password": data.password,
        })
    except Exception:
        raise ValueError("Invalid email or password")

    return AuthOutput(
        user_id=result.user.id,
        email=result.user.email,
        access_token=result.session.access_token,
    )