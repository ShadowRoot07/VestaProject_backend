from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from pydantic import BaseModel
from typing import List
from app.database import get_session
from app.models import User, Product, ProductLike
from app.core.security import get_current_user # Asegúrate de usar el que creamos en core

router = APIRouter(prefix="/products", tags=["products"])

class ProductCreate(BaseModel):
    title: str
    description: str
    price: float
    image_url: str
    affiliate_link: str
    category: str

@router.post("", status_code=status.HTTP_201_CREATED)
def create_product(
    product_data: ProductCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    new_product = Product(**product_data.dict(), owner_id=current_user.id)
    session.add(new_product)
    session.commit()
    session.refresh(new_product)
    return new_product

@router.get("", response_model=List[Product])
def get_products(session: Session = Depends(get_session)):
    return session.exec(select(Product)).all()

@router.get("/{product_id}")
def get_product(product_id: int, session: Session = Depends(get_session)):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product

@router.post("/{product_id}/like")
def toggle_like(
    product_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    statement = select(ProductLike).where(
        ProductLike.user_id == current_user.id,
        ProductLike.product_id == product_id
    )
    like = session.exec(statement).first()
    
    if like:
        session.delete(like)
        session.commit()
        return {"liked": False, "message": "Like eliminado"}
    
    new_like = ProductLike(user_id=current_user.id, product_id=product_id)
    session.add(new_like)
    session.commit()
    return {"liked": True, "message": "¡Like guardado!"}

