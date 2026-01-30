from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel
from .interactions import ProductLike



if TYPE_CHECKING:
    from .products import Product, ProductLike, Comment

class UserBase(SQLModel):
    username: str = Field(index=True, unique=True)
    email: str = Field(unique=True)

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str

    bio: Optional[str] = Field(default="¡Hola! Soy un nuevo desarrollador en Vesta.")
    profile_pic: Optional[str] = Field(default="https://ruta-por-defecto.com/avatar.png")
    website: Optional[str] = Field(default=None)
    
    products: List["Product"] = Relationship(back_populates="owner")
    liked_products: List["Product"] = Relationship(
        back_populates="favorited_by", 
        link_model=ProductLike
    )
    comments: List["Comment"] = Relationship(back_populates="user")


class UserPublic(BaseModel):
    username: str
    bio: Optional[str] = None
    profile_pic: Optional[str] = None
    website: Optional[str] = None
    total_reputation: int
    products_count: int
    products: List["Product"] = [] 

    class Config:
        from_attributes = True 

#UserPublic.model_rebuild()
