"""
Image Upload - core logic.

Responsibility: Accept image files, store them, save a pointer + metadata.

PRECONDITION:  valid project_id, supported file format, under size limit
POSTCONDITION: file exists in storage; Image row exists with analysis=null
"""
from .schemas import ImageUploadInput, ImageUploadOutput


def run(data: ImageUploadInput) -> ImageUploadOutput:
    """
    TODO: implement.
    This will read/write the database via the DB client.
    """
    raise NotImplementedError("Image Upload not implemented yet - this is a skeleton")
