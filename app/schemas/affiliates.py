from pydantic import BaseModel, field_validator
from typing import Optional
import bleach

class AffiliateLinkBase(BaseModel):
    platform_name: str
    url: str
    is_active: bool = True

    @field_validator("platform_name")
    @classmethod
    def sanitize_platform(cls, v):
        if v:
            return bleach.clean(v, tags=[], strip=True).strip()
        return v

class AffiliateLinkCreate(AffiliateLinkBase):
    product_id: int

class AffiliateLinkPublic(AffiliateLinkBase):
    id: int

