from pydantic import BaseModel, EmailStr

class Order(BaseModel):
    product_name: str
    size: str | None = None
    quantity: int
    total_price: float

class ShowOrder(Order):
    class Config: {
        "from_attributes": True
    }