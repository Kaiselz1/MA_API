from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from config.database import get_db
from config import oauth2
from api.user import user_schema
from api.favorite import favorite_model, favorite_schema

router = APIRouter(
    prefix="/favorites", 
    tags=["Favorites"]
)

# Add a product to favorites
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=favorite_schema.FavoriteResponse)
def add_favorite(
    request: favorite_schema.FavoriteCreate, 
    db: Session = Depends(get_db), 
    current_user: user_schema.User = Depends(oauth2.get_current_user)
):
    """Add a product to user's favorites"""
    try:
        new_favorite = favorite_model.Favorite(
            user_id=current_user.id,
            product_id=request.product_id
        )
        db.add(new_favorite)
        db.commit()
        db.refresh(new_favorite)
        return new_favorite
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product already in favorites"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# Get all favorites for current user
@router.get("/", status_code=status.HTTP_200_OK, response_model=favorite_schema.FavoritesListResponse)
def get_my_favorites(
    db: Session = Depends(get_db), 
    current_user: user_schema.User = Depends(oauth2.get_current_user)
):
    """Get all favorites for the current authenticated user"""
    favorites = db.query(favorite_model.Favorite).filter(
        favorite_model.Favorite.user_id == current_user.id
    ).order_by(favorite_model.Favorite.created_at.desc()).all()
    
    product_ids = [fav.product_id for fav in favorites]
    
    return {
        "user_id": current_user.id,
        "favorites": product_ids,
        "count": len(product_ids)
    }

# Get favorites for a specific user (admin only or same user)
@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=favorite_schema.FavoritesListResponse)
def get_user_favorites(
    user_id: int,
    db: Session = Depends(get_db), 
    current_user: user_schema.User = Depends(oauth2.get_current_user)
):
    """Get all favorites for a specific user"""
    # Only allow users to view their own favorites (you can add admin check here)
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view other users' favorites"
        )
    
    favorites = db.query(favorite_model.Favorite).filter(
        favorite_model.Favorite.user_id == user_id
    ).order_by(favorite_model.Favorite.created_at.desc()).all()
    
    product_ids = [fav.product_id for fav in favorites]
    
    return {
        "user_id": user_id,
        "favorites": product_ids,
        "count": len(product_ids)
    }

# Check if a product is in favorites
@router.get("/check/{product_id}", status_code=status.HTTP_200_OK)
def check_favorite(
    product_id: int,
    db: Session = Depends(get_db), 
    current_user: user_schema.User = Depends(oauth2.get_current_user)
):
    """Check if a product is in user's favorites"""
    favorite = db.query(favorite_model.Favorite).filter(
        favorite_model.Favorite.user_id == current_user.id,
        favorite_model.Favorite.product_id == product_id
    ).first()
    
    return {
        "user_id": current_user.id,
        "product_id": product_id,
        "is_favorite": favorite is not None
    }

# Remove a product from favorites
@router.delete("/{product_id}", status_code=status.HTTP_200_OK)
def remove_favorite(
    product_id: int,
    db: Session = Depends(get_db), 
    current_user: user_schema.User = Depends(oauth2.get_current_user)
):
    """Remove a product from user's favorites"""
    favorite = db.query(favorite_model.Favorite).filter(
        favorite_model.Favorite.user_id == current_user.id,
        favorite_model.Favorite.product_id == product_id
    )
    
    if not favorite.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Favorite not found"
        )
    
    favorite.delete(synchronize_session=False)
    db.commit()
    
    return {
        "message": "Favorite removed successfully",
        "user_id": current_user.id,
        "product_id": product_id
    }

# Clear all favorites for current user
@router.delete("/", status_code=status.HTTP_200_OK)
def clear_all_favorites(
    db: Session = Depends(get_db), 
    current_user: user_schema.User = Depends(oauth2.get_current_user)
):
    """Clear all favorites for the current user"""
    result = db.query(favorite_model.Favorite).filter(
        favorite_model.Favorite.user_id == current_user.id
    ).delete(synchronize_session=False)
    db.commit()
    
    return {
        "message": "All favorites cleared successfully",
        "user_id": current_user.id,
        "deleted_count": result
    }

# Add multiple products to favorites (batch)
@router.post("/batch", status_code=status.HTTP_201_CREATED)
def add_favorites_batch(
    request: favorite_schema.FavoriteBatchCreate,
    db: Session = Depends(get_db), 
    current_user: user_schema.User = Depends(oauth2.get_current_user)
):
    """Add multiple products to favorites at once"""
    added = []
    errors = []
    
    for product_id in request.product_ids:
        try:
            new_favorite = favorite_model.Favorite(
                user_id=current_user.id,
                product_id=product_id
            )
            db.add(new_favorite)
            db.flush()  # Flush to get the ID without committing
            added.append({
                "product_id": product_id,
                "id": new_favorite.id
            })
        except IntegrityError:
            db.rollback()
            errors.append({
                "product_id": product_id,
                "error": "Already in favorites"
            })
        except Exception as e:
            db.rollback()
            errors.append({
                "product_id": product_id,
                "error": str(e)
            })
    
    db.commit()
    
    return {
        "user_id": current_user.id,
        "added": added,
        "errors": errors,
        "added_count": len(added),
        "error_count": len(errors)
    }