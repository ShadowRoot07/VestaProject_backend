from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models.interactions import CartItem, ProductLike
from app.models.users import User
from app.core.security import get_current_user

router = APIRouter(prefix="/interactions", tags=["Interactions"])

@router.post("/like/{product_id}")
def toggle_like(product_id: int, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    # Buscamos si ya existe el like
    statement = select(ProductLike).where(ProductLike.user_id == current_user.id, ProductLike.product_id == product_id)
    like = session.exec(statement).first()

    if like:
        session.delete(like)
        msg = "Like removed"
    else:
        new_like = ProductLike(user_id=current_user.id, product_id=product_id)
        session.add(new_like)
        msg = "Like added"
    
    session.commit()
    return {"message": msg}

@router.post("/cart/{product_id}")
def add_to_cart(product_id: int, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    statement = select(CartItem).where(CartItem.user_id == current_user.id, CartItem.product_id == product_id)
    item = session.exec(statement).first()

    if item:
        item.quantity += 1
        session.add(item)
    else:
        new_item = CartItem(user_id=current_user.id, product_id=product_id, quantity=1)
        session.add(new_item)
    
    session.commit()
    return {"message": "Added to cart"}

