from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

class UserCreate(SQLModel):
    username: str
    email: str
    password: str # Usamos 'password' para recibirla y luego la hasheamos a 'hashed_password'

class ProductCreate(SQLModel):
    title: str
    description: str
    price: float
    image_url: str
    affiliate_link: str
    category: str
    owner_id: int

# Tabla de unión para Likes (Muchos a Muchos)
class ProductLike(SQLModel, table=True):
    user_id: int = Field(foreign_key="user.id", primary_key=True)
    product_id: int = Field(foreign_key="product.id", primary_key=True)

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(unique=True)
    hashed_password: str
    
    products: List["Product"] = Relationship(back_populates="owner")
    liked_products: List["Product"] = Relationship(
        back_populates="favorited_by", link_model=ProductLike
    )

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    price: float
    image_url: str
    affiliate_link: str
    category: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    owner_id: int = Field(foreign_key="user.id")
    owner: User = Relationship(back_populates="products")
    
    favorited_by: List[User] = Relationship(
        back_populates="liked_products", link_model=ProductLike
    )
    comments: List["Comment"] = Relationship(back_populates="product")

class Comment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    user_id: int = Field(foreign_key="user.id")
    product_id: int = Field(foreign_key="product.id")
    product: Product = Relationship(back_populates="comments")

