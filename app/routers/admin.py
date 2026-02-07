from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select, func
from typing import List

# Modelos y esquemas
from app.models.users import User
from app.models.products import Product
from app.models.interactions import Purchase
from app.models.categories import Category # Importación limpia aquí
from app.schemas.users import UserPublic
from app.core.security import get_current_admin_user
from app.database import get_session

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/stats")
def get_admin_stats(
    admin: User = Depends(get_current_admin_user),
    session: Session = Depends(get_session)
):
    total_users = session.exec(select(func.count(User.id))).one()
    total_products = session.exec(select(func.count(Product.id))).one()
    total_sales = session.exec(select(func.count(Purchase.id))).one()
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
    return session.exec(select(User)).all()

@router.get("/reports/categories")
def get_category_report(
    admin: User = Depends(get_current_admin_user),
    session: Session = Depends(get_session)
):
    statement = (
        select(Category.name, func.count(Purchase.id).label("total_sales"))
        .join(Product, Product.category_id == Category.id)
        .join(Purchase, Purchase.product_id == Product.id)
        .group_by(Category.name)
        .order_by(func.count(Purchase.id).desc())
    )

    results = session.exec(statement).all()
    return [{"category": r[0], "sales": r[1]} for r in results]

# UNIFICADO: Solo dejamos el método PATCH para evitar conflictos de nombres
@router.patch("/users/{user_id}/add-balance")
def admin_patch_balance(
    user_id: int,
    amount: float = Query(..., gt=0),
    admin: User = Depends(get_current_admin_user),
    session: Session = Depends(get_session)
):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    user.balance += amount
    session.add(user)
    session.commit()
    session.refresh(user)

    return {"message": "Saldo actualizado", "new_balance": user.balance}

@router.delete("/products/{product_id}")
def delete_product_admin(
    product_id: int,
    admin: User = Depends(get_current_admin_user),
    session: Session = Depends(get_session)
):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    session.delete(product)
    session.commit()
    return {"message": "Producto eliminado por el administrador"}

