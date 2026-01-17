import os
import shutil
from typing import Optional
from uuid import uuid4
from fastapi import UploadFile, HTTPException, status

ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/webp", "image/svg+xml"]
BASE_IMAGE_PATH = "static/images"
DEFAULT_IMAGE_NAME = "no_image.jpg"
DEFAULT_IMAGE_PATH = "/static/images/{DEFAULT_IMAGE_NAME}"

def save_image(image: Optional[UploadFile], sub_folder: str = "") -> str:
    """
    Save an uploaded image to disk and return its public URL
    If no image is provided, use a default image.
    """
    if not image:
        return DEFAULT_IMAGE_PATH

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



def delete_image(image_url: str, host_base_url: Optional[str] = None):
    """
    Delete an image from disk. Ignores default image.
    If host_base_url is provided, remove it from the URL to get the local path.
    """
    if not image_url or DEFAULT_IMAGE_NAME in image_url:
        return  # Do not delete default image

    # Convert full URL to local path if host_base_url is given
    if host_base_url and image_url.startswith(host_base_url):
        image_path = image_url.replace(host_base_url.rstrip("/"), ".")
    else:
        image_path = "." + image_url  # relative path

    if os.path.exists(image_path):
        os.remove(image_path)



def replace_image(old_image_url: str, new_image: Optional[UploadFile], sub_folder: str = "", host_base_url: Optional[str] = None) -> str:
    """
    Replace an old image with a new one.
    Returns the URL of the new image.
    """
    # Delete old image
    delete_image(old_image_url, host_base_url)

    # Save new image (or default)
    local_image_url = save_image(new_image, sub_folder)

    # Return full URL if host_base_url is provided
    if host_base_url:
        return f"{host_base_url.rstrip('/')}{local_image_url}"

    # Save new image (or default if None)
    return local_image_url