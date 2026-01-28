from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import Session, select
from app.database import get_session, create_db_and_tables
from app.models import User, Product, Comment, ProductLike
from app.auth_utils import hash_password, create_access_token
from pydantic import BaseModel

app = FastAPI(title="VestaAPI")

# --- ESQUEMAS PARA VALIDACIÓN (Evitan errores de Neovim) ---
class UserRegister(BaseModel):
    username: str
    email: str
    password: str

class ProductCreate(BaseModel):
    title: str
    description: str
    price: float
    image_url: str
    affiliate_link: str
    category: str
    owner_id: int

# --- ENDPOINTS ---

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/auth/register", status_code=status.HTTP_201_CREATED)
def register(user_data: UserRegister, session: Session = Depends(get_session)):
    # Verificamos si el usuario ya existe para evitar errores de DB
    existing_user = session.exec(select(User).where(User.email == user_data.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hash_password(user_data.password)
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return {"message": "Usuario creado exitosamente", "id": new_user.id}

@app.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(product_data: ProductCreate, session: Session = Depends(get_session)):
    new_product = Product(**product_data.dict())
    session.add(new_product)
    session.commit()
    session.refresh(new_product)
    return new_product

@app.post("/products/{product_id}/like")
def like_product(product_id: int, user_id: int, session: Session = Depends(get_session)):
    # Verificamos si el producto existe
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
        
    new_like = ProductLike(user_id=user_id, product_id=product_id)
    session.add(new_like)
    session.commit()
    return {"message": "¡Like guardado!"}

