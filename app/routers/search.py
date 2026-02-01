from fastapi import APIRouter, Depends
from sqlmodel import Session, select, or_
from typing import List, Optional
from app.database import get_session
from app.models import Product

router = APIRouter(prefix="/search", tags=["Search"])

@router.get("", response_model=List[Product])
def search_products(
    q: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    sort_by: str = "newest", # newest, lowest_price, highest_price
    limit: int = Query(default=20, le=50),
    session: Session = Depends(get_session)
):
    statement = select(Product)

    if q:
        statement = statement.where(
            or_(
                Product.title.icontains(q),
                Product.description.icontains(q)
            )
        )

    if min_price is not None:
        statement = statement.where(Product.price >= min_price)
    if max_price is not None:
        statement = statement.where(Product.price <= max_price)

    if sort_by == "lowest_price":
        statement = statement.order_by(Product.price.asc())
    elif sort_by == "highest_price":
        statement = statement.order_by(Product.price.desc())
    else:
        statement = statement.order_by(Product.created_at.desc())

    return session.exec(statement.limit(limit)).all()

