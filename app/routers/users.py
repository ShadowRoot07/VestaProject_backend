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


@router.put("/me")
def update_my_profile(
    user_data: dict, # Luego podemos crear un esquema Pydantic para esto
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    current_user.bio = user_data.get("bio", current_user.bio)
    current_user.profile_pic = user_data.get("profile_pic", current_user.profile_pic)
    current_user.website = user_data.get("website", current_user.website)
    
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return {"message": "Perfil actualizado", "user": current_user}



@router.get("/{username}")
def get_user_profile(
    username: str,
    session: Session = Depends(get_session)
):
    # Buscamos al usuario por su nombre
    statement = select(User).where(User.username == username)
    user = session.exec(statement).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Preparamos la respuesta con sus productos
    return {
        "username": user.username,
        "bio": user.bio,
        "profile_pic": user.profile_pic,
        "website": user.website,
        "joined_at": user.id, # Opcional: podrías usar un campo created_at
        "products_count": len(user.products),
        "products": user.products # Esto lista sus publicaciones
    }

