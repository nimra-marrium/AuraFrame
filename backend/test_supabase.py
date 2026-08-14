import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

if not url or not key:
    print("❌ SUPABASE_URL or SUPABASE_KEY is missing from .env")
    exit()

try:
    supabase = create_client(url, key)
    print("✅ Supabase connection initialized successfully!")
    print("Project URL:", url)
except Exception as e:
    print("❌ Connection failed:")
    print(e)