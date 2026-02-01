from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select
from typing import Optional, List
import jose
from app.database import get_session
from app.models.affiliates import AffiliateLink, ClickEvent
from app.schemas.affiliates import AffiliateLinkCreate
from app.models.users import User
from app.models.products import Product
from app.core.security import ALGORITHM, SECRET_KEY, get_current_user

router = APIRouter(prefix="/affiliates", tags=["Affiliates"])

def get_optional_user_id(request: Request) -> Optional[int]:
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None
    try:
        token = auth_header.split(" ")[1]
        payload = jose.jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id_raw = payload.get("sub")
        # Ensure we return an int if it's a numeric ID
        return int(user_id_raw) if user_id_raw and str(user_id_raw).isdigit() else None
    except Exception:
        return None

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

@router.get("/go/{link_id}")
def redirect_and_track(
    link_id: int,
    request: Request,
    session: Session = Depends(get_session)
):
    link = session.get(AffiliateLink, link_id)
    if not link or not link.is_active:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid or inactive link")

    new_click = ClickEvent(
        link_id=link.id,
        user_id=get_optional_user_id(request),
        referrer=request.headers.get("referer")
    )
    session.add(new_click)
    session.commit()
    return RedirectResponse(url=link.url)

@router.get("/product/{product_id}", response_model=List[AffiliateLink])
def get_product_links(product_id: int, session: Session = Depends(get_session)):
    statement = select(AffiliateLink).where(
        AffiliateLink.product_id == product_id,
        AffiliateLink.is_active == True
    )
    return session.exec(statement).all()

@router.get("/analytics/{product_id}")
def get_product_analytics(
    product_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    product = session.get(Product, product_id)
    if not product or product.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    stats = [
        {
            "platform": link.platform_name,
            "total_clicks": len(link.clicks),
            "unique_users": len({c.user_id for c in link.clicks if c.user_id})
        }
        for link in product.affiliate_links
    ]
    return {"product_title": product.title, "analytics": stats}

