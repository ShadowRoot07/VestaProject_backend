from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from .interactions import ProductLike

if TYPE_CHECKING:
    from .products import Product, Comment

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(unique=True)
    hashed_password: str
    bio: Optional[str] = Field(default="Hello! I am a new developer on Vesta.")
    profile_pic: Optional[str] = Field(default="https://default-path.com/avatar.png")
    website: Optional[str] = None
    reputation: int = Field(default=0)
    is_admin: bool = Field(default=False) # Adding the admin flag we discussed

    products: List["Product"] = Relationship(back_populates="owner")
    liked_products: List["Product"] = Relationship(
        back_populates="favorited_by",
        link_model=ProductLike
    )
    comments: List["Comment"] = Relationship(back_populates="user")

