from typing import List
from fastapi import APIRouter, status, Depends, HTTPException
from config.database import get_db
from sqlalchemy.orm import Session
from api.category import category_schema, category_model

router = APIRouter(
    prefix='/category',
    tags=['Category']
)

# Create Category
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=category_schema.ShowCategory)
def create_category(request: category_schema.Category, db: Session = Depends(get_db)):
    new_category = category_model.Category(
        name = request.name,
        description = request.description,
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

# Get Category
@router.get('/', status_code=status.HTTP_200_OK, response_model=List[category_schema.Category])
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(category_model.Category).all()
    if not categories:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='No categories found'
        )
    return categories

# Get Category by id
@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=category_schema.Category)
def get_category_by_id(id: int, db: Session = Depends(get_db)):
    category = db.query(category_model).filter(category_model.Category.id == id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No category id {id} is not found'
        )
    return category

# Delete Category
@router.delete('/{id}', status_code=status.HTTP_200_OK)
def delete_category(id: int, db: Session = Depends(get_db)):
    category = db.query(category_model.Category).filter(category_model.Category.id == id)
    if not category.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    category.delete(synchronize_session=False)
    db.commit()
    return {"detail": "Category deleted successfully"}

# Update Category
@router.put('/{id}',  status_code=status.HTTP_200_OK)
def update_category(id: int, request: category_schema.Category, db: Session = Depends(get_db)):
    category = db.query(category_model.Category).filter(category_model.Category.id == id)
    if not category.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'no category id {id} is not found'
        )
    category.update({
        "name": request.name,
        "description": request.description
    })
    db.commit()
    return {"detail": "Category updated successfully"}