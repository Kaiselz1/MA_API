from sqlalchemy import Column, Integer, String
from config.database import base
from sqlalchemy.orm import relationship

class Category(base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    image_url = Column(String, unique=True, nullable=True)
    # figure out later on
    # total_products = Column(Integer, default=0)

    products = relationship("Product", back_populates="category")