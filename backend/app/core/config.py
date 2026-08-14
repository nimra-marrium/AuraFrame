"""
Central place for environment variables / secrets.
NEVER hardcode API keys anywhere else in the codebase - always import from here.
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    AI_API_KEY: str = os.getenv("AI_API_KEY", "")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

settings = Settings()
