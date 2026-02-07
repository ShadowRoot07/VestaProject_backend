from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select, func
from typing import List
from app.database import get_session
from app.models.users import User
from app.models.products import Product
from app.models.interactions import Purchase
from app.schemas.users import UserPublic
from app.core.security import get_current_admin_user

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/stats")
def get_admin_stats(
    admin: User = Depends(get_current_admin_user), 
    session: Session = Depends(get_session)
):
    # Contamos todo para el dashboard
    total_users = session.exec(select(func.count(User.id))).one()
    total_products = session.exec(select(func.count(Product.id))).one()
    total_sales = session.exec(select(func.count(Purchase.id))).one()
    
    # Sumamos todo el dinero que se ha movido en compras
    # (Usamos el precio guardado en el momento de la compra)
    revenue = session.exec(select(func.sum(Purchase.price_at_purchase))).one() or 0

    return {
        "total_users": total_users,
        "total_products": total_products,
        "total_sales": total_sales,
        "total_revenue": revenue
    }

@router.get("/users", response_model=List[UserPublic])
def list_all_users(
    admin: User = Depends(get_current_admin_user),
    session: Session = Depends(get_session)
):
    # El admin puede ver a todos los registrados
    users = session.exec(select(User)).all()
    return users

