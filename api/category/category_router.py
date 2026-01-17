from typing import List, Optional
from fastapi import APIRouter, status, Depends, HTTPException, UploadFile, File, Form, Request
from config.database import get_db
from sqlalchemy.orm import Session
from utils.image_handler import save_image, delete_image, replace_image
from api.category import category_schema, category_model

router = APIRouter(
    prefix='/category',
    tags=['Category']
)

# Fix for both file and JSON
def category_form(name: str = Form(...), description: Optional[str] = Form(None)) -> category_schema.Category:
    return category_schema.Category(
        name=name,
        description=description,
    )



# Create Category
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=category_schema.ShowCategory)
def create_category(host: Request, request: category_schema.Category = Depends(category_form), image: Optional[UploadFile] = File(None), db: Session = Depends(get_db)):
    local_image_url = save_image(image, sub_folder="categories")
    base_url = str(host.base_url)
    host_image_url = f"{base_url.rstrip('/')}{local_image_url}"

    new_category = category_model.Category(
        name = request.name,
        description = request.description,
        image_url = host_image_url
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

# Get Category
@router.get('/', status_code=status.HTTP_200_OK, response_model=List[category_schema.ShowCategory])
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(category_model.Category).all()
    if not categories:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='No categories found'
        )
    return categories

# Get Category by id
@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=category_schema.ShowCategory)
def get_category_by_id(id: int, db: Session = Depends(get_db)):
    category = db.query(category_model.Category).filter(category_model.Category.id == id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No category id {id} is not found'
        )
    return category

# Delete Category
@router.delete('/{id}', status_code=status.HTTP_200_OK)
def delete_category(id: int, db: Session = Depends(get_db)):
    category = db.query(category_model.Category).filter(category_model.Category.id == id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    delete_image(category.image_url)
    db.delete(category)
    # category.delete(synchronize_session=False)
    db.commit()
    return {"detail": "Category deleted successfully"}

# Update Category
@router.put('/{id}',  status_code=status.HTTP_200_OK)
def update_category(id: int, request: category_schema.Category = Depends(category_form), image: Optional[UploadFile] = File(None), host: Request = None, db: Session = Depends(get_db)):
    category = db.query(category_model.Category).filter(category_model.Category.id == id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'no category id {id} is not found'
        )
    base_url = str(host.base_url) if host else None
    category.image_url = replace_image(
        old_image_url=category.image_url,
        new_image=image,
        sub_folder="categories",
        host_base_url=base_url
    )

    category.name = request.name
    category.description = request.description
    db.commit()
    db.refresh(category)
    return {"detail": "Category updated successfully"}