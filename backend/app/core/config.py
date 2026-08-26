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
    SUPABASE_SERVICE_KEY: str = os.getenv("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InB4bnFod2lxcG5mZW1kZ3NmdGx4Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4NjcxNTcwNywiZXhwIjoyMTAyMjkxNzA3fQ.5TiLzTWbzIZwm0bkqj6ItCrPu1iTs9v2ggwqgFX-JUM", "")

settings = Settings()
