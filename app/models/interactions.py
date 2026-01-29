from sqlmodel import SQLModel, Field
from sqlalchemy import UniqueConstraint

class ProductLike(SQLModel, table=True):
    __table_args__ = (UniqueConstraint("user_id", "product_id", name="unique_user_product_like"),)
    user_id: int = Field(foreign_key="user.id", primary_key=True)
    product_id: int = Field(foreign_key="product.id", primary_key=True)

