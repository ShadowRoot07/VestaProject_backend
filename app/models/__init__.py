from .interactions import ProductLike
from .users import User
from .products import Product, Comment

# Esto fuerza a SQLModel a conectar los cables internos 
# de las relaciones 'back_populates'
User.model_rebuild()
Product.model_rebuild()
Comment.model_rebuild()

# Exportamos para que main.py los encuentre
__all__ = ["User", "Product", "Comment", "ProductLike"]

