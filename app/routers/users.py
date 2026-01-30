from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from app.database import get_session
from app.models import User, Product, UserPublic, UserUpdate
from app.core.security import get_current_user
from sqlalchemy.orm import selectinload

router = APIRouter(prefix="/users", tags=["users"])

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


@router.put("/me", response_model=UserPublic)
def update_my_profile(
    user_data: UserUpdate, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Actualiza el perfil del usuario autenticado de forma dinámica.
    """
    # Convertimos el esquema a diccionario, ignorando los campos no enviados
    update_data = user_data.model_dump(exclude_unset=True)
    
    # Aplicamos los cambios al objeto de la base de datos
    for key, value in update_data.items():
        setattr(current_user, key, value)
    
    session.add(current_user)
    session.commit()
    session.refresh(current_user) # Recargamos para obtener los datos frescos de la DB

    # Calculamos la reputación para devolver el objeto UserPublic completo
    total_likes = sum(len(product.favorited_by) for product in current_user.products)
    
    # Construimos la respuesta manualmente para cumplir con UserPublic
    return {
        **current_user.model_dump(),
        "total_reputation": total_likes,
        "products_count": len(current_user.products),
        "products": current_user.products
    }


@router.get("/{username}", response_model=UserPublic)
def get_user_profile(
    username: str,
    session: Session = Depends(get_session)
):
    # 1. Buscamos al usuario
    statement = select(User).where(User.username == username).options(selectinload(User.products))
    user = session.exec(statement).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # 2. Cálculo de reputación
    total_likes = sum(len(product.favorited_by) for product in user.products)

    # 3. Retornamos el objeto con los nombres de campos que espera UserPublic
    return {
        "username": user.username,
        "bio": user.bio,
        "profile_pic": user.profile_pic,
        "website": user.website,
        "total_reputation": total_likes,
        "products_count": len(user.products),
        "products": user.products
    }

