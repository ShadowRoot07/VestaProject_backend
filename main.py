from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import Session, select
from app.database import get_session, create_db_and_tables
from app.models import User, Product, Comment, ProductLike
from app.core.auth_utils import hash_password, create_access_token
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlmodel import SQLModel

SQLModel.metadata.naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

# Importamos tus herramientas desde tu archivo
from app.core.auth_utils import (
    SECRET_KEY, 
    ALGORITHM, 
    verify_password, 
    create_access_token
)

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

# --- FUNCIONES PARA LA VALIDACION. ---

# Esto es lo que FastAPI usa para saber de dónde sacar el token en los Swagger Docs
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# --- LA FUNCIÓN QUE USA TUS HERRAMIENTAS ---
def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    try:
        # Aquí usamos tu SECRET_KEY y ALGORITHM para abrir el candado
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Error al validar token")
        
    user = session.exec(select(User).where(User.username == username)).first()
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    return user

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
def create_product(
    product_data: ProductCreate, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user) # <--- AQUÍ ESTÁ EL CANDADO
):
    # Usamos los datos del esquema + el ID del usuario autenticado
    new_product = Product(
        **product_data.dict(), 
        owner_id=current_user.id
    )
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


@app.post("/auth/token")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    session: Session = Depends(get_session)
):
    # 1. Buscar al usuario por su nombre (username)
    user = session.exec(select(User).where(User.username == form_data.username)).first()
    
    # 2. Validar existencia y contraseña
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. Crear el Token
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# 1. Obtener todos los productos (El Feed Principal)
@app.get("/products")
def get_products(session: Session = Depends(get_session)):
    products = session.exec(select(Product)).all()
    return products

# 2. Obtener un producto específico por ID (Vista de detalle)
@app.get("/products/{product_id}")
def get_product(product_id: int, session: Session = Depends(get_session)):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product

# 3. Mis Productos (Filtrado por el usuario logueado)
@app.get("/me/products")
def get_my_products(
    session: Session = Depends(get_session), 
    current_user: User = Depends(get_current_user)
):
    # Solo traemos los productos donde owner_id sea el del usuario del Token
    statement = select(Product).where(Product.owner_id == current_user.id)
    products = session.exec(statement).all()
    return products
