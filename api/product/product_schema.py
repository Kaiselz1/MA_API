from pydantic import BaseModel, HttpUrl

class Product(BaseModel):
    name: str
    description: str
    price: float
    category_id: int

class ShowProduct(Product):
    image_url: HttpUrl

    class Config:{
        'from_attribute': True
    }
