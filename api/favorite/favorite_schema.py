from pydantic import BaseModel
from datetime import datetime
from typing import List

class FavoriteCreate(BaseModel):
    product_id: int

class FavoriteResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class FavoritesListResponse(BaseModel):
    user_id: int
    favorites: List[int]
    count: int

class FavoriteBatchCreate(BaseModel):
    product_ids: List[int]