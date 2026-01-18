# Add these fields to your existing User model
# If you already have a User model, just add the phone and address columns

from sqlalchemy import Column, Integer, String
from config.database import base

class User(base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)