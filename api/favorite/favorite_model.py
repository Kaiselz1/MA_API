from sqlalchemy import Column, Integer, String, DateTime, Index
from sqlalchemy.sql import func
from config.database import base

class Favorite(base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    product_id = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Composite unique constraint to prevent duplicates
    __table_args__ = (
        Index('idx_user_product', 'user_id', 'product_id', unique=True),
    )