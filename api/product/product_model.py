from sqlalchemy import Column, Integer, String, Float, ForeignKey
from config.database import base
from sqlalchemy.orm import relationship

class Product(base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    image_url = Column(String, unique=True, nullable=True)
    category_id = Column(String, ForeignKey('categories.id'), nullable=False)

    category = relationship("Category", back_populates="products")

