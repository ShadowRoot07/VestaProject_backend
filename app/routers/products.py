from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select
from typing import List
from app.database import get_session
from app.models.products import Product
from app.models.users import User
from app.schemas.products import ProductCreate, ProductUpdate
from app.models.interactions import ProductLike
from app.core.security import get_current_user
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/products", tags=["Products"], redirect_slashes=False)

@router.get("", response_model=List[Product])
def get_products(
    offset: int = 0,
    limit: int = Query(default=100, le=100),
    session: Session = Depends(get_session)
):
    return session.exec(select(Product).offset(offset).limit(limit)).all()

@router.post("", response_model=Product, status_code=status.HTTP_201_CREATED)
def create_product(
    product_in: ProductCreate, # Using sanitized schema
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    # Convert schema to DB model and attach owner
    new_product = Product(**product_in.model_dump(), owner_id=current_user.id)
    
    session.add(new_product)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid category_id: {product_in.category_id} does not exist."
        )

    session.refresh(new_product)
    return new_product

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


@router.post("/{product_id}/like", status_code=status.HTTP_200_OK)
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
        if owner: owner.reputation -= 1 # Resta reputación si quitan el like
        message = "Like removed"
    else:
        new_like = ProductLike(user_id=current_user.id, product_id=product_id)
        session.add(new_like)
        if owner: owner.reputation += 1 # Suma reputación si dan like
        message = "Like added"

    session.commit()
    session.refresh(product)
    if owner: session.refresh(owner)

    return {
        "message": message,
        "likes_count": product.likes_count,
        "owner_reputation": owner.reputation if owner else 0
    }

