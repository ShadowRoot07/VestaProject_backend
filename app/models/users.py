from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel
from .interactions import ProductLike # <--- Agrega esto arriba

if TYPE_CHECKING:
    from .products import Product, ProductLike, Comment

class UserBase(SQLModel):
    username: str = Field(index=True, unique=True)
    email: str = Field(unique=True)

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    
    products: List["Product"] = Relationship(back_populates="owner")
    liked_products: List["Product"] = Relationship(
        back_populates="favorited_by", 
        link_model=ProductLike
    )
    comments: List["Comment"] = Relationship(back_populates="user") 
