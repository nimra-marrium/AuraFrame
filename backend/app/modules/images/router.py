"""
Image Upload - HTTP interface. Stays THIN - delegates to service.py.
"""
from fastapi import APIRouter, HTTPException
from .schemas import ImageUploadInput, ImageUploadOutput
from . import service

router = APIRouter()


@router.post("/", response_model=ImageUploadOutput)
def handle_images(payload: ImageUploadInput):
    try:
        return service.run(payload)
    except NotImplementedError:
        raise HTTPException(status_code=501, detail="Image Upload not implemented yet")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
