from pydantic import BaseModel, HttpUrl

class Category(BaseModel):
    name: str
    description: str
    

class ShowCategory(Category):
    id: int
    image_url: HttpUrl

    class Config:{
        'from_attributes': True
    }