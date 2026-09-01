"""
Auth module - core logic.
"""
from app.core.database import get_supabase
from app.core.logging import get_logger
from .schemas import SignupInput, LoginInput, AuthOutput

logger = get_logger(__name__)


def signup(data: SignupInput) -> AuthOutput:
    supabase = get_supabase()

    try:
        result = supabase.auth.sign_up({
            "email": data.email,
            "password": data.password,
        })
    except Exception as e:
        logger.error(f"Signup failed for {data.email}: {e}")
        raise ValueError(f"Signup failed: {str(e)}")

    if result.user is None:
        logger.error(f"Signup returned no user for {data.email}")
        raise ValueError("Signup failed - email may already be registered")

    token = result.session.access_token if result.session else ""
    logger.info(f"User signed up: {result.user.id}")

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
    except Exception as e:
        logger.error(f"Login failed for {data.email}: {e}")
        raise ValueError("Invalid email or password")

    logger.info(f"User logged in: {result.user.id}")

    return AuthOutput(
        user_id=result.user.id,
        email=result.user.email,
        access_token=result.session.access_token,
    )