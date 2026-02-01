from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select
from typing import Optional, List
import jose
from app.database import get_session
from app.models.affiliates import AffiliateLink, ClickEvent
from app.schemas.affiliates import AffiliateLinkCreate # Imported from schemas
from app.models.users import User
from app.models.products import Product
from app.core.security import ALGORITHM, SECRET_KEY, get_current_user

router = APIRouter(prefix="/affiliates", tags=["Affiliates"])

# ... (get_optional_user_id remains same) ...

@router.post("", response_model=AffiliateLink, status_code=status.HTTP_201_CREATED)
def create_affiliate_link(
    data: AffiliateLinkCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    product = session.get(Product, data.product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    if product.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")

    new_link = AffiliateLink(**data.model_dump())
    session.add(new_link)
    session.commit()
    session.refresh(new_link)
    return new_link

# ... (other endpoints remain same, ensure they import properly) ...

