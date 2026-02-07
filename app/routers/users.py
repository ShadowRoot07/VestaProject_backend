from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select, func
from typing import List
from app.database import get_session
from app.models.users import User
from app.models.products import Product
from app.schemas.users import UserPublic, UserUpdate
from app.models.interactions import CartItem, Purchase, ProductLike
from app.core.security import get_current_user
from sqlalchemy.orm import selectinload

router = APIRouter(prefix="/users", tags=["Users"])

# ... (get_my_products remains same) ...

@router.get("/me", response_model=UserPublic)
def get_my_profile(current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    # ... (tus consultas anteriores de cart_items y liked_items) ...

    # Traemos las compras (Purchases)
    # Aquí puedes hacer un join para traer los detalles del producto comprado
    purchases = session.exec(
        select(Product).join(Purchase).where(Purchase.user_id == current_user.id)
    ).all()

    user_data = UserPublic.model_validate(current_user)
    user_data.cart_items = cart_items
    user_data.liked_items = liked_items
    
    # Inyectamos la lista de productos comprados y el conteo
    user_data.purchases_items = purchases # Asegúrate de añadir esto a UserPublic en schemas
    user_data.purchases_count = len(purchases)

    return user_data


@router.put("/me", response_model=UserPublic)
def update_my_profile(
    user_data: UserUpdate, # Sanitization happens here automatically
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    update_dict = user_data.model_dump(exclude_unset=True)

    for key, value in update_dict.items():
        # Si incluiste password en UserUpdate, hay que hashearla antes de guardarla
        if key == "password" and value:
            from app.core.auth_utils import hash_password
            value = hash_password(value)
        setattr(current_user, key, value)

    session.add(current_user)
    session.commit()
    session.refresh(current_user)

    # Cálculo dinámico para la respuesta UserPublic
    reputation = sum(len(p.favorited_by) for p in current_user.products)

    return {
        **current_user.model_dump(),
        "total_reputation": reputation,
        "products_count": len(current_user.products),
        "products": current_user.products
    }
# ... (get_user_profile remains same) ...

