from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

# 1. Tabla de Usuarios
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(unique=True)
    hashed_password: str
    
    # Relaciones
    products: List["Product"] = Relationship(back_populates="owner")

# 2. Tabla de Productos
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

# 3. Tabla para Clicks y Seguimiento
class Click(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    confirmed_purchase: bool = Field(default=False)
    
    user_id: int = Field(foreign_key="user.id")
    product_id: int = Field(foreign_key="product.id")

