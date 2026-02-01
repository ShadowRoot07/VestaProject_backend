from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from app.database import get_session
from app.models.categories import Category
from app.models.users import User
from app.core.security import get_current_admin_user 
from sqlalchemy.exc import IntegrityError
import re # Para validar slugs manualmente si fuera necesario

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get("", response_model=List[Category])
def get_categories(session: Session = Depends(get_session)):
    """Public endpoint to list all categories."""
    return session.exec(select(Category)).all()

@router.post("", response_model=Category, status_code=status.HTTP_201_CREATED)
def create_category(
    category: Category,
    session: Session = Depends(get_session),
    current_admin: User = Depends(get_current_admin_user) 
):
    """
    Protected endpoint: Only users with is_admin=True can create categories.
    """
    # Blindaje 1: Normalización de datos
    category.slug = category.slug.lower().replace(" ", "-")
    
    # Blindaje 2: Validación de formato de slug (Solo letras, números y guiones)
    if not re.match(r'^[a-z0-9-]+$', category.slug):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Slug must contain only lowercase letters, numbers, and hyphens."
        )

    try:
        session.add(category)
        session.commit()
        session.refresh(category)
        return category
    except IntegrityError:
        session.rollback()
        # Blindaje 3: Error informativo para el cliente
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Category with slug '{category.slug}' or name '{category.name}' already exists."
        )

