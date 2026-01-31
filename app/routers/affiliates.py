from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select
from typing import Optional
import jose
#--- Importacion de modelos ---
from app.database import get_session
from app.models.affiliates import AffiliateLink, ClickEvent
from app.core.security import ALGORITHM, SECRET_KEY

router = APIRouter(prefix="/affiliates", tags=["affiliates"])

def get_optional_user_id(request: Request) -> Optional[int]:
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None
    
    try:
        token = auth_header.split(" ")[1]
        payload = jose.jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id_raw = payload.get("sub")
        return user_id_raw
    except Exception:
        return None

@router.get("/go/{link_id}")
def redirect_and_track(
    link_id: int, 
    request: Request,
    session: Session = Depends(get_session)
):
    link = session.get(AffiliateLink, link_id)
    if not link or not link.is_active:
        raise HTTPException(status_code=404, detail="Enlace no válido o inactivo")

    user_id = get_optional_user_id(request)

    new_click = ClickEvent(
        link_id=link.id,
        user_id=user_id,
        referrer=request.headers.get("referer") 
    )
    
    session.add(new_click)
    session.commit()
    
    return RedirectResponse(url=link.url)
