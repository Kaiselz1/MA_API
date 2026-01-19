from fastapi import APIRouter, status

router = APIRouter(
    prefix="/orders",
    tags=["order"]
)

router.post('/', status_code=status.HTTP_201_CREATED)
def create_order():
    return {"message": "Order created"}