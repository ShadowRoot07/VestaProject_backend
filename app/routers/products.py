from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select, func
from typing import List, Optional
from app.database import get_session
from app.models.products import Product
from app.models.users import User
from app.schemas.products import ProductCreate, ProductUpdate
from app.models.interactions import ProductLike, CartItem # Importamos CartItem también
from app.core.security import get_current_user
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/products", tags=["Products"], redirect_slashes=False)

def get_optional_user(
    session: Session = Depends(get_session), 
    current_user: Optional[User] = Depends(get_current_user)
) -> Optional[User]:
    return current_user

@router.get("", response_model=List[dict]) # Usamos dict para enviar campos dinámicos
def get_products(
    offset: int = 0,
    limit: int = Query(default=100, le=100),
    session: Session = Depends(get_session),
    current_user: Optional[User] = Depends(get_current_user) # Cambiado para que sea inyectado si existe
):
    products = session.exec(select(Product).offset(offset).limit(limit)).all()
    
    # IDs de productos con Like y en Carrito del usuario actual
    liked_ids = []
    cart_ids = []
    if current_user:
        liked_ids = session.exec(select(ProductLike.product_id).where(ProductLike.user_id == current_user.id)).all()
        cart_ids = session.exec(select(CartItem.product_id).where(CartItem.user_id == current_user.id)).all()

    result = []
    for p in products:
        p_data = p.model_dump()
        p_data["is_liked_by_me"] = p.id in liked_ids
        p_data["is_in_cart"] = p.id in cart_ids
        # Calculamos el total de likes en tiempo real
        likes_count = session.exec(select(func.count(ProductLike.user_id)).where(ProductLike.product_id == p.id)).one()
        p_data["likes_count"] = likes_count
        result.append(p_data)
        
    return result

@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    if product.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to delete this product"
        )

    session.delete(product)
    session.commit()
    return {"message": "Product deleted successfully"}

@router.post("/{product_id}/like")
def toggle_product_like(
    product_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    owner = session.get(User, product.owner_id)

    statement = select(ProductLike).where(
        ProductLike.user_id == current_user.id,
        ProductLike.product_id == product_id
    )
    existing_like = session.exec(statement).first()

    if existing_like:
        session.delete(existing_like)
        if owner: owner.reputation -= 1
        message = "Like removed"
    else:
        new_like = ProductLike(user_id=current_user.id, product_id=product_id)
        session.add(new_like)
        if owner: owner.reputation += 1
        message = "Like added"

    session.commit()
    
    # Obtenemos el nuevo conteo de likes después del cambio
    likes_count = session.exec(select(func.count(ProductLike.user_id)).where(ProductLike.product_id == product_id)).one()

    return {
        "message": message,
        "is_liked": not existing_like,
        "likes_count": likes_count,
        "owner_reputation": owner.reputation if owner else 0
    }
