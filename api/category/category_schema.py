from pydantic import BaseModel

class Category(BaseModel):
    name: str
    description: str

class ShowCategory(Category):
    class Config:{
        'from_attributes': True
    }