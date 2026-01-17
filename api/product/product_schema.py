from pydantic import BaseModel, HttpUrl

class Product(BaseModel):
    name: str
    description: str
    price: float
    category_id: int

class ShowProduct(BaseModel):
    id: int
    name: str
    description: str
    price: float
    image_url: HttpUrl
    category_name: str

    class Config:{
        'from_attribute': True
    }
