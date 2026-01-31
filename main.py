from fastapi import FastAPI
from sqlmodel import SQLModel
from app.database import create_db_and_tables
from app.routers import auth, products, users, search
from app.models.users import UserPublic
from app.models.products import Product
from app.routers import affiliates
from app.models.affiliates import AffiliateLink


UserPublic.model_rebuild()

# Configuración de convenciones (mantenla aquí)
SQLModel.metadata.naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

app = FastAPI(title="VestaAPI")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Inclusión de routers
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(users.router)
app.include_router(search.router)
app.include_router(affiliates.router)

# Puedes mover el endpoint /me/products a un router de 'users' o dejarlo en products

