from fastapi import APIRouter, Depends
from sqlmodel import Session, select, or_, col
from typing import List, Optional
from app.database import get_session
from app.models import Product

router = APIRouter(prefix="/search", tags=["search"])

@router.get("", response_model=List[Product])
def advanced_search(
    q: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    sort_by: Optional[str] = "newest", # newest, lowest_price, highest_price
    session: Session = Depends(get_session),
    limit: int = 20
):
    statement = select(Product)

    # 1. Búsqueda por texto (Título o Descripción)
    if q:
        statement = statement.where(
            or_(
                Product.title.contains(q),
                Product.description.contains(q)
            )
        )

    # 2. Filtro de Rango de Precios
    if min_price is not None:
        statement = statement.where(Product.price >= min_price)
    if max_price is not None:
        statement = statement.where(Product.price <= max_price)

    # 3. Ordenamiento
    if sort_by == "lowest_price":
        statement = statement.order_by(Product.price.asc())
    elif sort_by == "highest_price":
        statement = statement.order_by(Product.price.desc())
    else:
        # Por defecto: los más recientes primero
        statement = statement.order_by(Product.created_at.desc())

    results = session.exec(statement.limit(limit)).all()
    return results

