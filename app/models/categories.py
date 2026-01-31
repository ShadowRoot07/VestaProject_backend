from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .products import Product

class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    description: Optional[str] = None
    slug: str = Field(unique=True) # Para URLs bonitas como /categories/laptops-gaming

    # Relación: Una categoría tiene muchos productos
    products: List["Product"] = Relationship(back_populates="category_rel")

