from sqlalchemy import Column, Integer, String, Float
from config.database import base

class Order(base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, nullable=False)
    size = Column(String, nullable=True)
    quantity = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)