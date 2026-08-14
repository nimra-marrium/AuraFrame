"""
Single shared Supabase client. Every module that needs DB/auth access
imports get_supabase() from here - nobody creates their own connection.
This is the "core" dependency every module is allowed to share.
"""

from supabase import create_client, Client
from app.core.config import settings


_client: Client | None = None


def get_supabase() -> Client:
    global _client

    if _client is None:
        if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
            raise RuntimeError(
                "SUPABASE_URL / SUPABASE_KEY missing - check your .env file"
            )

        _client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_KEY
        )

    return _client