import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine, Session

load_dotenv()

# Asegúrate de tener DATABASE_URL en tu archivo .env
sqlite_url = os.getenv("DATABASE_URL")

# El echo=True sirve para ver en consola todas las consultas SQL que se ejecutan (útil para aprender)
engine = create_engine(
    sqlite_url, 
    echo=True,
    pool_pre_ping=True,  # Verifica si la conexión está viva antes de usarla
    connect_args={"connect_timeout": 10} # Da un poco más de tiempo para conectar
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

