from fastapi import APIRouter, status
from api.order import order_schema

router = APIRouter(
    prefix="/orders",
    tags=["order"]
)

@router.post('/', status_code=status.HTTP_201_CREATED)
def create_order():
    return {"message": "Order Created"}