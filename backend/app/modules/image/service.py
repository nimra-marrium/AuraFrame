"""
Image Upload module - core logic.
"""
import uuid
from app.core.database import get_supabase
from app.core.logging import get_logger
from .schemas import ImageOutput

logger = get_logger(__name__)

ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}
MAX_FILE_SIZE_BYTES = 8 * 1024 * 1024
BUCKET_NAME = "images"


def upload(project_id: str, filename: str, content_type: str, file_bytes: bytes) -> ImageOutput:
    if content_type not in ALLOWED_CONTENT_TYPES:
        raise ValueError(f"unsupported file type: {content_type}")

    if len(file_bytes) > MAX_FILE_SIZE_BYTES:
        raise ValueError("file too large - max 8MB")

    supabase = get_supabase()
    ext = filename.split(".")[-1] if "." in filename else "jpg"
    storage_path = f"{project_id}/{uuid.uuid4()}.{ext}"

    try:
        supabase.storage.from_(BUCKET_NAME).upload(
            storage_path, file_bytes, {"content-type": content_type},
        )
        public_url = supabase.storage.from_(BUCKET_NAME).get_public_url(storage_path)

        result = supabase.table("images").insert({
            "project_id": project_id,
            "url": public_url,
        }).execute()
    except Exception as e:
        logger.error(f"Image upload failed for project {project_id}: {e}")
        raise ValueError(f"failed to upload image: {e}")

    if not result.data:
        logger.error(f"Image insert returned no data for project {project_id}")
        raise ValueError("failed to save image record")

    logger.info(f"Image uploaded for project {project_id}: {result.data[0]['id']}")
    return ImageOutput(**result.data[0])


def list_for_project(project_id: str) -> list[ImageOutput]:
    supabase = get_supabase()
    try:
        result = supabase.table("images").select("*").eq("project_id", project_id).execute()
    except Exception as e:
        logger.error(f"Image list failed for project {project_id}: {e}")
        raise ValueError(f"failed to list images: {e}")

    return [ImageOutput(**row) for row in result.data]