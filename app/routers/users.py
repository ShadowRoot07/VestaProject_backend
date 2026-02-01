from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from app.database import get_session
from app.models import User, Product, UserPublic, UserUpdate
from app.core.security import get_current_user
from sqlalchemy.orm import selectinload

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me/products", response_model=List[Product])
def get_my_products(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get all products owned by the authenticated user"""
    statement = select(Product).where(Product.owner_id == current_user.id)
    return session.exec(statement).all()

@router.get("/me", response_model=User)
def get_my_profile(current_user: User = Depends(get_current_user)):
    """Get basic profile info of the authenticated user"""
    return current_user

@router.put("/me", response_model=UserPublic)
def update_my_profile(
    user_data: UserUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Update authenticated user profile dynamically"""
    update_dict = user_data.model_dump(exclude_unset=True)

    for key, value in update_dict.items():
        setattr(current_user, key, value)

    session.add(current_user)
    session.commit()
    session.refresh(current_user)

    reputation = sum(len(p.favorited_by) for p in current_user.products)

    return {
        **current_user.model_dump(),
        "total_reputation": reputation,
        "products_count": len(current_user.products),
        "products": current_user.products
    }

@router.get("/{username}", response_model=UserPublic)
def get_user_profile(username: str, session: Session = Depends(get_session)):
    """Public profile view for any user"""
    statement = select(User).where(User.username == username).options(selectinload(User.products))
    user = session.exec(statement).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    reputation = sum(len(p.favorited_by) for p in user.products)

    return {
        **user.model_dump(),
        "total_reputation": reputation,
        "products_count": len(user.products),
        "products": user.products
    }

