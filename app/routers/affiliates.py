from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select
from typing import Optional
import jose
#--- Importacion de modelos ---
from app.database import get_session
from app.models.affiliates import AffiliateLink, ClickEvent, AffiliateLinkCreate
from app.models import User, Product
from app.core.security import ALGORITHM, SECRET_KEY, get_current_user


router = APIRouter(prefix="/affiliates", tags=["affiliates"])

def get_optional_user_id(request: Request) -> Optional[int]:
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return None

    try:
        token = auth_header.split(" ")[1]
        payload = jose.jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id_raw = payload.get("sub")
        
        # IMPORTANTE: Convertimos a int porque SQLModel/Postgres 
        # espera un número para la relación con el Usuario.
        return int(user_id_raw) if user_id_raw else None 
        
    except Exception:
        return None


@router.post("/", response_model=AffiliateLink)
def create_affiliate_link(
    data: AffiliateLinkCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    # 1. Verificar que el producto existe y pertenece al usuario
    product = session.get(Product, data.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    if product.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para editar este producto")

    # 2. Crear el enlace
    new_link = AffiliateLink(
        platform_name=data.platform_name,
        url=data.url,
        product_id=data.product_id
    )
    
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



@router.get("/product/{product_id}", response_model=list[AffiliateLink])
def get_product_links(
    product_id: int,
    session: Session = Depends(get_session)
):
    """
    Retorna todos los enlaces de afiliados de un producto específico.
    Este es público para que los compradores vean dónde comprar.
    """
    statement = select(AffiliateLink).where(AffiliateLink.product_id == product_id, AffiliateLink.is_active == True)
    links = session.exec(statement).all()
    return links



@router.get("/analytics/{product_id}")
def get_product_analytics(
    product_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    # Verificar propiedad
    product = session.get(Product, product_id)
    if not product or product.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Acceso denegado")

    stats = []
    for link in product.affiliate_links:
        stats.append({
            "platform": link.platform_name,
            "total_clicks": len(link.clicks),
            "unique_users": len(set(c.user_id for c in link.clicks if c.user_id))
        })
    
    return {
        "product": product.name,
        "analytics": stats
    }


@router.patch("/{link_id}", response_model=AffiliateLink)
def update_affiliate_link(
    link_id: int,
    data: AffiliateLinkCreate, # Reutilizamos el esquema de creación
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    link = session.get(AffiliateLink, link_id)
    if not link:
        raise HTTPException(status_code=404, detail="Enlace no encontrado")
    
    # Verificar que el producto del link pertenece al usuario
    if link.product.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso")

    # Actualizar campos
    link.platform_name = data.platform_name
    link.url = data.url
    
    session.add(link)
    session.commit()
    session.refresh(link)
    return link

@router.delete("/{link_id}")
def deactivate_affiliate_link(
    link_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    link = session.get(AffiliateLink, link_id)
    if not link or link.product.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="No autorizado")

    # En lugar de borrar de la DB, lo desactivamos (Soft Delete)
    link.is_active = False
    session.add(link)
    session.commit()
    return {"message": "Enlace desactivado correctamente"}

