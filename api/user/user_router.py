from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db
from config.security import hash
from config import oauth2
from api.user import user_model, user_schema

router = APIRouter(
    prefix="/users", 
    tags=["Users"]
)

# Create User
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=user_schema.ShowUser)
def create_user(request: user_schema.User, db: Session = Depends(get_db), current_user: user_schema.User = Depends(oauth2.get_current_user)):
    existing_user = db.query(user_model.User).filter(user_model.User.email == request.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    new_user = user_model.User(
        username=request.username, 
        email=request.email, 
        password=hash.hash_password(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Get All Users
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[user_schema.ShowUser])
def get_users(db: Session = Depends(get_db), current_user: user_schema.User = Depends(oauth2.get_current_user)):
    users = db.query(user_model.User).all()
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="No users found"
        )
    return users

# Get User by ID
@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=user_schema.ShowUser)
def get_user_by_id(id: int, db: Session = Depends(get_db), current_user: user_schema.User = Depends(oauth2.get_current_user)):
    user = db.query(user_model.User).filter(user_model.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"User with id {id} not found"
        )
    return user

# Delete User
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db), current_user: user_schema.User = Depends(oauth2.get_current_user)):
    user = db.query(user_model.User).filter(user_model.User.id == id)
    if not user.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"User with id {id} not found"
        )
    user.delete(synchronize_session=False)
    db.commit()
    return {"detail": "User deleted successfully"}

# Update User
@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_user(id: int, request: user_schema.User, db: Session = Depends(get_db), current_user: user_schema.User = Depends(oauth2.get_current_user)):
    # find user in db
    user = db.query(user_model.User).filter(user_model.User.id == id)
    if not user.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"User with id {id} not found"
        )
    user.update({
        "username": request.username,
        "email": request.email,
        "password": request.password
    })  
    db.commit()
    return {"detail": "User updated successfully"}