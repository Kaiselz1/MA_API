import os
import shutil
from typing import Optional
from uuid import uuid4
from fastapi import UploadFile, HTTPException, status

ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/webp"]
BASE_IMAGE_PATH = "static/images"
DEFAULT_IMAGE_PATH = "/static/images/no_image.jpg"

def save_image(image: Optional[UploadFile], sub_folder: str = "") -> str:
    """
    Save an uploaded image to disk and return its public URL
    If no image is provided, use a default image.
    """
    if not image:
        return f"/static/images/{DEFAULT_IMAGE_PATH}"

    if image.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid image type"
        )

    folder_path = os.path.join(BASE_IMAGE_PATH, sub_folder)
    os.makedirs(folder_path, exist_ok=True)

    ext = os.path.splitext(image.filename)[1]
    filename = f"{uuid4()}{ext}"

    file_path = os.path.join(folder_path, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    return f"/static/images/{sub_folder}/{filename}".replace("//", "/")