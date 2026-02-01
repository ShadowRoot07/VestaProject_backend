from pydantic import BaseModel
from typing import Optional

class AffiliateLinkBase(BaseModel):
    platform_name: str
    url: str
    is_active: bool = True

class AffiliateLinkCreate(AffiliateLinkBase):
    product_id: int

class AffiliateLinkPublic(AffiliateLinkBase):
    id: int

