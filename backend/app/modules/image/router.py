"""
Image Upload module - HTTP interface.

Unlike other modules, this one accepts multipart/form-data (a real file
upload), not JSON - that's why it uses UploadFile + Form instead of a
Pydantic schema for the request body.
"""
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from .schemas import ImageOutput
from . import service

router = APIRouter()


@router.post("/", response_model=ImageOutput)
async def upload_image(
    project_id: str = Form(...),
    file: UploadFile = File(...),
):
    try:
        file_bytes = await file.read()
        return service.upload(
            project_id=project_id,
            filename=file.filename,
            content_type=file.content_type,
            file_bytes=file_bytes,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/project/{project_id}", response_model=list[ImageOutput])
def list_images(project_id: str):
    return service.list_for_project(project_id)