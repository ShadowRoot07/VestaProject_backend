from fastapi import APIRouter, Depends, Query # Added Query
from sqlmodel import Session, select, or_
from typing import List, Optional
from app.database import get_session
from app.models.products import Product # Specific import

router = APIRouter(prefix="/search", tags=["Search"])

@router.get("", response_model=List[Product])
def search_products(
    q: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    sort_by: str = "newest", # Options: newest, lowest_price, highest_price
    limit: int = Query(default=20, le=50),
    session: Session = Depends(get_session)
):
    statement = select(Product)

    # 1. Full-text search (Title or Description)
    if q:
        statement = statement.where(
            or_(
                Product.title.icontains(q),
                Product.description.icontains(q)
            )
        )

    # 2. Price Range Filtering
    if min_price is not None:
        statement = statement.where(Product.price >= min_price)
    if max_price is not None:
        statement = statement.where(Product.price <= max_price)

    # 3. Sorting Logic
    if sort_by == "lowest_price":
        statement = statement.order_by(Product.price.asc())
    elif sort_by == "highest_price":
        statement = statement.order_by(Product.price.desc())
    else:
        # Default: Newest first
        statement = statement.order_by(Product.created_at.desc())

    results = session.exec(statement.limit(limit)).all()
    return results

