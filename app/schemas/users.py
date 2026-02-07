from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, List, Any
import bleach

class UserBase(BaseModel):
    username: str
    email: EmailStr
    bio: Optional[str] = None
    profile_pic: Optional[str] = None
    website: Optional[str] = None
    balance: float

    @field_validator("username", "bio")
    @classmethod
    def sanitize_text(cls, v, info):
        if v:
            clean_v = bleach.clean(v, tags=[], strip=True).strip()
            return clean_v
        return v

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    bio: Optional[str] = None
    profile_pic: Optional[str] = None
    website: Optional[str] = None
    password: Optional[str] = None

    @field_validator("bio")
    @classmethod
    def sanitize_bio(cls, v):
        if v:
            return bleach.clean(v, tags=[], strip=True).strip()
        return v

class UserPublic(UserBase):
    id: int
    reputation: int
    is_admin: bool
    # Listas dinámicas para el perfil
    cart_items: List[Any] = []
    liked_items: List[Any] = []
    purchases_items: List[Any] = [] # <--- ¡ESTE FALTABA!
    purchases_count: int = 0

    class Config:
        from_attributes = True

