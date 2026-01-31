from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models.categories import Category

router = APIRouter(prefix="/categories", tags=["categories"])

@router.get("/", response_model=list[Category])
def get_categories(session: Session = Depends(get_session)):
    return session.exec(select(Category)).all()

@router.post("/", response_model=Category)
def create_category(category: Category, session: Session = Depends(get_session)):
    # Lógica simple para crear, puedes añadir seguridad después
    session.add(category)
    session.commit()
    session.refresh(category)
    return category

