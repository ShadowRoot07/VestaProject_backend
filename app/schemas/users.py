from pydantic import BaseModel, EmailStr
from typing import Optional, List

class UserBase(BaseModel):
    username: str
    email: EmailStr
    bio: Optional[str] = None
    profile_pic: Optional[str] = None
    website: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    bio: Optional[str] = None
    profile_pic: Optional[str] = None
    website: Optional[str] = None
    password: Optional[str] = None

class UserPublic(UserBase):
    id: int
    total_reputation: int
    products_count: int
    # We use a string reference or dynamic import to avoid circularity with Product
    products: List = [] 

    class Config:
        from_attributes = True

