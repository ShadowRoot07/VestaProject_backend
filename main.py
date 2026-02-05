from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from app.database import create_db_and_tables
from app.routers import auth, products, users, search, affiliates, categories, comments

app = FastAPI(title="VestaAPI")

# CORS Setup
origins = ["http://localhost:3000", "http://localhost:5173", "https://your-vesta-domain.com", "*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database Naming Convention
SQLModel.metadata.naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Include Routers
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(users.router)
app.include_router(search.router)
app.include_router(affiliates.router)
app.include_router(categories.router)
app.include_router(comments.router)
