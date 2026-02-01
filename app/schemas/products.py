from pydantic import BaseModel, field_validator
from typing import Optional
import bleach

class ProductBase(BaseModel):
    title: str
    description: str
    price: float
    image_url: Optional[str] = "https://via.placeholder.com/150"
    category_id: int

    @field_validator("title", "description")
    @classmethod
    def sanitize_product_data(cls, v):
        if v:
            # Eliminamos cualquier intento de inyección de código
            return bleach.clean(v, tags=[], strip=True).strip()
        return v

    @field_validator("price")
    @classmethod
    def validate_price(cls, v):
        if v < 0:
            raise ValueError("Price cannot be negative")
        return v

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    image_url: Optional[str] = None
    category_id: Optional[int] = None

    @field_validator("title", "description")
    @classmethod
    def sanitize_update(cls, v):
        if v:
            return bleach.clean(v, tags=[], strip=True).strip()
        return v

