from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

# Importamos las clases de enlace y relación
from .interactions import ProductLike
from .affiliates import AffiliateLink
from .categories import Category

# Solo para tipado estático
if TYPE_CHECKING:
    from .users import User

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    price: float
    image_url: Optional[str] = Field(default="https://via.placeholder.com/150")
    # Se eliminó el campo individual 'affiliate_link' porque ahora usamos la relación One-to-Many

    # Llave foránea y relación
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    category_rel: Optional[Category] = Relationship(back_populates="products")

    created_at: datetime = Field(default_factory=datetime.utcnow)

    @property
    def likes_count(self) -> int:
        return len(self.favorited_by)

    # Relación con el dueño
    owner_id: int = Field(foreign_key="user.id")
    owner: Optional["User"] = Relationship(back_populates="products")

    # Relación con comentarios
    comments: List["Comment"] = Relationship(
        back_populates="product",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

    # Relación de Likes (Muchos a Muchos)
    favorited_by: List["User"] = Relationship(
        back_populates="liked_products",
        link_model=ProductLike,
    )

    # Esta es la relación que reemplaza al campo eliminado
    affiliate_links: List["AffiliateLink"] = Relationship(back_populates="product")


class Comment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    user_id: int = Field(foreign_key="user.id")
    product_id: int = Field(foreign_key="product.id")

    product: Product = Relationship(back_populates="comments")
    user: "User" = Relationship(back_populates="comments")

