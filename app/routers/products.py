from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import List, Optional
from app.database import get_session
from app.models.products import Product
from app.models.users import User
from app.core.security import get_current_user
# Usamos redirect_slashes=False para que /products funcione sin /
router = APIRouter(prefix="/products", tags=["products"], redirect_slashes=False)

@router.get("", response_model=List[Product])
def get_products(
    offset: int = 0,
    limit: int = Query(default=100, le=100),
    session: Session = Depends(get_session)
):
    """Listar todos los productos"""
    return session.exec(select(Product).offset(offset).limit(limit)).all()

@router.post("", response_model=Product)
def create_product(
    product_data: Product, # Usamos el modelo directo para simplificar por ahora
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Crear un producto vinculado a una categoría y a un dueño"""
    
    # 1. Verificar que el owner_id sea el del usuario logueado
    product_data.owner_id = current_user.id
    
    # 2. El category_id ya viene en product_data según tu modelo
    session.add(product_data)
    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=400, 
            detail=f"Error al crear producto: Asegúrate de que la categoría {product_data.category_id} exista."
        )
        
    session.refresh(product_data)
    return product_data

@router.get("/{product_id}", response_model=Product)
def get_product(product_id: int, session: Session = Depends(get_session)):
    """Obtener un producto específico"""
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product

@router.delete("/{product_id}")
def delete_product(
    product_id: int, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Borrar un producto (solo el dueño puede)"""
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    if product.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para borrar este producto")
        
    session.delete(product)
    session.commit()
    return {"message": "Producto eliminado"}

