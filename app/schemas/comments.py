from pydantic import BaseModel

class CommentCreate(BaseModel):
    product_id: int
    content: str

