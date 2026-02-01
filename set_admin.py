from sqlmodel import Session, select
from app.database import engine
from app.models.users import User

def make_admin(username: str):
    with Session(engine) as session:
        statement = select(User).where(User.username == username)
        user = session.exec(statement).first()
        if user:
            user.is_admin = True
            session.add(user)
            session.commit()
            print(f"¡{username} ahora es Administrador! 🚀")
        else:
            print("Usuario no encontrado.")

if __name__ == "__main__":
    make_admin("ShadowRoot07")

