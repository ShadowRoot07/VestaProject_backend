from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from typing import List
from app.database import get_session
from app.models import User, Product
from app.core.security import get_current_user

router = APIRouter(prefix="/me", tags=["profile"])

@router.get("/products", response_model=List[Product])
def get_my_products(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Retorna la lista de productos que el usuario actual ha publicado.
    """
    statement = select(Product).where(Product.owner_id == current_user.id)
    products = session.exec(statement).all()
    return products

@router.get("/profile", response_model=User)
def get_my_profile(current_user: User = Depends(get_current_user)):
    """
    Retorna la información básica del perfil del usuario logueado.
    """
    return current_user

