from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from app.database import get_session
from app.models.categories import Category
from app.models.users import User
from app.core.security import get_current_admin_user # New dependency
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get("", response_model=List[Category])
def get_categories(session: Session = Depends(get_session)):
    return session.exec(select(Category)).all()

@router.post("", response_model=Category, status_code=status.HTTP_201_CREATED)
def create_category(
    category: Category, 
    session: Session = Depends(get_session),
    admin_user: User = Depends(get_current_admin_user) # Only admins can enter here
):
    try:
        session.add(category)
        session.commit()
        session.refresh(category)
        return category
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Category with slug '{category.slug}' already exists."
        )

