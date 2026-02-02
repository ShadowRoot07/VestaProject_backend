from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

# Importación para el tipado sin causar círculos
if TYPE_CHECKING:
    from .products import Product
    from .users import User

class AffiliateLinkBase(SQLModel):
    platform_name: str
    url: str
    is_active: bool = Field(default=True)

class AffiliateLink(AffiliateLinkBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="product.id")

    # Relaciones
    product: "Product" = Relationship(back_populates="affiliate_links")
    clicks: List["ClickEvent"] = Relationship(back_populates="affiliate_link")

class ClickEvent(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    link_id: int = Field(foreign_key="affiliatelink.id")
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    referrer: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    affiliate_link: AffiliateLink = Relationship(back_populates="clicks")

