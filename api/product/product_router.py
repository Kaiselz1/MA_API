from typing import List, Optional
from fastapi import APIRouter, Depends, status, HTTPException, UploadFile, File, Form, Request
from sqlalchemy.orm import Session
from config.database import get_db
from utils.image_handler import save_image, delete_image, replace_image
from api.product import product_schema, product_model

router = APIRouter(
   prefix='/products',
   tags=['Product'] 
)

# Fix for both file and JSON
def product_form(name: str = Form(...), description: Optional[str] = Form(None), price: float = Form(...), category_id: int = Form(...)) -> product_schema.Product:
    return product_schema.Product(
        name=name,
        description=description,
        price=price,
        category_id=category_id
    )



# Create Product
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=product_schema.ShowProduct)
def create_product(host: Request, request: product_schema.Product = Depends(product_form), image: Optional[UploadFile] = File(None), db: Session = Depends(get_db)):
    local_image_url = save_image(image, sub_folder="products")
    base_url = str(host.base_url)
    host_image_url = f"{base_url.rstrip('/')}{local_image_url}"

    new_product = product_model.Product(
        name = request.name,
        description = request.description,
        price = request.price,
        image_url = host_image_url,
        category_id = request.category_id
    )
    
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    show_product = product_schema.ShowProduct(
        id=new_product.id,
        name=new_product.name,
        description=new_product.description,
        price=new_product.price,
        image_url=new_product.image_url,
        category_name=new_product.category.name if new_product.category else None
    )

    return show_product

# Get Products
@router.get('/', status_code=status.HTTP_200_OK, response_model=List[product_schema.ShowProduct])
def get_products(db: Session = Depends(get_db)):
    products = db.query(product_model.Product).all()
    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='No products found'
        )
    product_with_category_name = []
    for product in products:
        product_with_category_name.append(product_schema.ShowProduct(
            id=product.id,
            name=product.name,
            description=product.description,
            price=product.price,
            image_url=product.image_url,
            category_name=product.category.name if product.category else None
        ))

    return product_with_category_name

# Get Products by id
@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=product_schema.ShowProduct)
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    product = db.query(product_model.Product).filter(product_model.Product.id == id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No product id {id} is not found'
        )
    product = product_schema.ShowProduct(
        id=product.id,
        name=product.name,
        description=product.description,
        price=product.price,
        image_url=product.image_url,
        category_name=product.category.name if product.category else None
    )
    
    return product

# Delete Product
@router.delete('/{id}', status_code=status.HTTP_200_OK)
def delete_product(id: int, db: Session = Depends(get_db)):
    product = db.query(product_model.Product).filter(product_model.Product.id == id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    delete_image(product.image_url)
    db.delete(product)
    # product.delete(synchronize_session=False)
    db.commit()

    return {"detail": "Product deleted successfully"}

# Update Product
@router.put('/{id}',  status_code=status.HTTP_200_OK)
def update_product(id: int, request: product_schema.Product = Depends(product_form), image: Optional[UploadFile] = File(None), host: Request = None, db: Session = Depends(get_db)):
    product = db.query(product_model.Product).filter(product_model.Product.id == id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No product id {id} is not found'
        )
    
    base_url = str(host.base_url) if host else None
    product.image_url = replace_image(
        old_image_url=product.image_url,
        new_image=image,
        sub_folder="products",
        host_base_url=base_url
    )
    
    product.name = request.name
    product.description = request.description
    product.price = request.price
    product.category_id = request.category_id

    db.commit()
    db.refresh(product)
    return {"detail": "Product updated successfully"}