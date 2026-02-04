from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
import bleach
from app.database import get_session
from app.models.products import Comment, Product
from app.models.users import User
from app.core.security import get_current_user
from app.schemas.comments import CommentCreate


router = APIRouter(prefix="/comments", tags=["Comments"])


@router.post("", status_code=status.HTTP_201_CREATED)
def create_comment(
    comment_in: CommentCreate, # <--- Usamos el Schema aquí
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    product = session.get(Product, comment_in.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Sanitización con el contenido del schema
    clean_content = bleach.clean(comment_in.content, tags=[], strip=True)

    new_comment = Comment(
        content=clean_content,
        product_id=comment_in.product_id,
        user_id=current_user.id
    )

    session.add(new_comment)
    session.commit()
    session.refresh(new_comment)
    return new_comment
