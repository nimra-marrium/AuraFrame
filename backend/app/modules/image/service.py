"""
Image Upload module - core logic.

Responsibility: accept image bytes, store them, save a pointer + metadata.

PRECONDITION:  valid project_id, file is a supported format, under size limit
POSTCONDITION: file exists in Supabase Storage; Image row exists with analysis=null

Testable standalone: call upload() with fake bytes + a fake project_id,
no HTTP layer needed, just a real Supabase connection.
"""
import uuid
from app.core.database import get_supabase
from .schemas import ImageOutput

ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}
MAX_FILE_SIZE_BYTES = 8 * 1024 * 1024  # 8 MB
BUCKET_NAME = "images"


def upload(project_id: str, filename: str, content_type: str, file_bytes: bytes) -> ImageOutput:
    if content_type not in ALLOWED_CONTENT_TYPES:
        raise ValueError(f"unsupported file type: {content_type}")

    if len(file_bytes) > MAX_FILE_SIZE_BYTES:
        raise ValueError("file too large - max 8MB")

    supabase = get_supabase()

    # unique storage path so filenames never collide
    ext = filename.split(".")[-1] if "." in filename else "jpg"
    storage_path = f"{project_id}/{uuid.uuid4()}.{ext}"

    supabase.storage.from_(BUCKET_NAME).upload(
        storage_path,
        file_bytes,
        {"content-type": content_type},
    )

    public_url = supabase.storage.from_(BUCKET_NAME).get_public_url(storage_path)

    result = supabase.table("images").insert({
        "project_id": project_id,
        "url": public_url,
    }).execute()

    if not result.data:
        raise ValueError("failed to save image record")

    return ImageOutput(**result.data[0])


def list_for_project(project_id: str) -> list[ImageOutput]:
    supabase = get_supabase()
    result = supabase.table("images").select("*").eq("project_id", project_id).execute()
    return [ImageOutput(**row) for row in result.data]