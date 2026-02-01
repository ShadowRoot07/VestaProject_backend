from .interactions import ProductLike
from .users import User
from .products import Product, Comment
from .affiliates import AffiliateLink, ClickEvent
from .categories import Category

# Rebuild internal SQLModel relations
User.model_rebuild()
Product.model_rebuild()
Comment.model_rebuild()
AffiliateLink.model_rebuild()
Category.model_rebuild()

__all__ = ["User", "Product", "Comment", "ProductLike", "AffiliateLink", "ClickEvent", "Category"]

