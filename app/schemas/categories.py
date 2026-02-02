# app/schemas/categories.py
from pydantic import BaseModel, field_validator
from typing import Optional
import bleach

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    slug: str

    @field_validator("name", "description", "slug")
    @classmethod
    def sanitize_category(cls, v):
        if v:
            return bleach.clean(v, tags=[], strip=True).strip()
        return v

class CategoryCreate(CategoryBase):
    pass

class CategoryPublic(CategoryBase):
    id: int

