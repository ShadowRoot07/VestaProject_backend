from fastapi import FastAPI
from app.database import create_db_and_tables
from app.models import User, Product, Click # Importamos para que SQLModel los registre

app = FastAPI(title="VestaAPI")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def home():
    return {"status": "VestaAPI is Online", "database": "Connected to Neon"}

