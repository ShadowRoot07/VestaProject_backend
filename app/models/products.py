from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from .interactions import ProductLike
from .affiliates import AffiliateLink


if TYPE_CHECKING:
    from .users import User


class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    price: float
    image_url: Optional[str] = Field(default="https://via.placeholder.com/150")
    affiliate_link: Optional[str] = Field(default=None)
    category: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    @property
    def likes_count(self) -> int:
        return len(self.favorited_by)

    owner_id: int = Field(foreign_key="user.id")
    owner: "User" = Relationship(back_populates="products")
    comments: List["Comment"] = Relationship(
        back_populates="product",
        cascade_delete=True 
    )

    favorited_by: List["User"] = Relationship(
        back_populates="liked_products",
        link_model=ProductLike,
    )
    affiliate_links: List["AffiliateLink"] = Relationship(back_populates="product")



class Comment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    user_id: int = Field(foreign_key="user.id")
    product_id: int = Field(foreign_key="product.id")
    product: Product = Relationship(back_populates="comments")
    user: "User" = Relationship(back_populates="comments")

