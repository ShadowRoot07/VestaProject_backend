from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jose.jwt
from sqlmodel import Session, select
from app.database import get_session
from app.models.users import User
from .security_config import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jose.jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            # Aquí faltaba la instrucción que causaba el error
            raise credentials_exception
    except jose.jwt.JWTError:
        raise credentials_exception

    user = session.exec(select(User).where(User.username == username)).first()

    if user is None:
        raise credentials_exception

    return user

def get_current_admin_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user does not have enough privileges"
        )
    return current_user

