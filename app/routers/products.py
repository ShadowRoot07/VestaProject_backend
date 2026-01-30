from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from pydantic import BaseModel
from typing import List
from app.database import get_session
from app.models import User, Product, ProductLike
from app.core.security import get_current_user
from app.models import Comment
from sqlalchemy.orm import selectinload

router = APIRouter(prefix="/products", tags=["products"])

class ProductCreate(BaseModel):
    title: str
    description: str
    price: float
    image_url: str
    affiliate_link: str
    category: str


class CommentCreate(BaseModel):
    content: str


@router.post("", status_code=status.HTTP_201_CREATED)
def create_product(
    product_data: ProductCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    new_product = Product(**product_data.dict(), owner_id=current_user.id)
    session.add(new_product)
    session.commit()
    session.refresh(new_product)
    return new_product

@router.get("", response_model=List[Product])
def get_products(session: Session = Depends(get_session)):
    return session.exec(select(Product)).all()



@router.get("/{product_id}")
def get_product(product_id: int, session: Session = Depends(get_session)):
    statement = (
        select(Product)
        .where(Product.id == product_id)
        .options(selectinload(Product.comments))
    )
    product = session.exec(statement).first()

    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    product_data = product.model_dump()
    product_data["comments"] = [
    {
        **c.model_dump(),
        "username": c.user.username
    } for c in product.comments
    ]
    product_data["likes_count"] = product.likes_count
    
    return product_data



@router.post("/{product_id}/like")
def toggle_like(
    product_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    statement = select(ProductLike).where(
        ProductLike.user_id == current_user.id,
        ProductLike.product_id == product_id
    )
    like = session.exec(statement).first()
    
    if like:
        session.delete(like)
        session.commit()
        return {"liked": False, "message": "Like eliminado"}
    
    new_like = ProductLike(user_id=current_user.id, product_id=product_id)
    session.add(new_like)
    session.commit()
    return {"liked": True, "message": "¡Like guardado!"}


@router.post("/{product_id}/comments", status_code=status.HTTP_201_CREATED)
def create_comment(
    product_id: int,
    comment_data: CommentCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    # 1. Verificar si el producto existe
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # 2. Crear el comentario
    new_comment = Comment(
        content=comment_data.content,
        product_id=product_id,
        user_id=current_user.id
    )
    session.add(new_comment)
    session.commit()
    session.refresh(new_comment)
    return new_comment

@router.delete("/comments/{comment_id}")
def delete_comment(
    comment_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    comment = session.get(Comment, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comentario no encontrado")
    
    # SEGURIDAD: Solo el dueño puede borrarlo
    if comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso para borrar este comentario")
    
    session.delete(comment)
    session.commit()
    return {"message": "Comentario eliminado"}


@router.put("/{product_id}")
def update_product(
    product_id: int,
    product_data: ProductCreate, # Usamos el mismo esquema de creación
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    # 🔒 VALIDACIÓN: ¿Es el dueño?
    if product.owner_id != current_user.id:
        raise HTTPException(
            status_code=403, 
            detail="No tienes permiso para editar este producto"
        )

    # Actualizamos los campos
    data_dict = product_data.dict(exclude_unset=True)
    for key, value in data_dict.items():
        setattr(product, key, value)
    
    session.add(product)
    session.commit()
    session.refresh(product)
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    if product.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="No autorizado")

    # Limpiamos manualmente los likes (la relación muchos-a-muchos)
    # Esto elimina las filas en la tabla 'productlike' sin borrar a los usuarios
    product.favorited_by = [] 
    session.add(product)
    
    # Ahora sí, borramos el producto (esto disparará el cascade en comentarios)
    session.delete(product)
    session.commit()
    return None

