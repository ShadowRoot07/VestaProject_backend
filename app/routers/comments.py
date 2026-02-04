from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
import bleach
from app.database import get_session
from app.models.products import Comment, Product
from app.models.users import User
from app.core.security import get_current_user

router = APIRouter(prefix="/comments", tags=["Comments"])

@router.post("", status_code=status.HTTP_201_CREATED)
def create_comment(
    product_id: int,
    content: str,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    # 1. Verificar si el producto existe
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # 2. Sanitización contra XSS (Bleach)
    # Limpiamos etiquetas HTML no deseadas
    clean_content = bleach.clean(content, tags=[], strip=True)

    # 3. Crear el comentario
    new_comment = Comment(
        content=clean_content,
        product_id=product_id,
        user_id=current_user.id
    )

    session.add(new_comment)
    session.commit()
    session.refresh(new_comment)
    return new_comment

@router.delete("/{comment_id}")
def delete_comment(
    comment_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    comment = session.get(Comment, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    # Solo el autor o un admin puede borrar
    if comment.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not allowed to delete this comment")

    session.delete(comment)
    session.commit()
    return {"message": "Comment deleted successfully"}

