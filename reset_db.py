from sqlalchemy import text
from sqlmodel import SQLModel
from app.database import engine
# Importar modelos para la creación posterior
from app.models.users import User
from app.models.products import Product
from app.models.categories import Category
from app.models.affiliates import AffiliateLink, ClickEvent

def reset_database():
    with engine.connect() as connection:
        print("⚠️  Borrando tablas con CASCADE...")
        # Esto borra las tablas ignorando el orden de las llaves foráneas
        connection.execute(text("DROP TABLE IF EXISTS clickevent CASCADE;"))
        connection.execute(text("DROP TABLE IF EXISTS affiliatelink CASCADE;"))
        connection.execute(text("DROP TABLE IF EXISTS product CASCADE;"))
        connection.execute(text("DROP TABLE IF EXISTS category CASCADE;"))
        connection.execute(text("DROP TABLE IF EXISTS \"user\" CASCADE;"))
        connection.commit()
    
    print("🏗️  Creando nuevas tablas desde cero...")
    SQLModel.metadata.create_all(engine)
    print("✅ ¡Base de datos limpia y actualizada!")

if __name__ == "__main__":
    reset_database()

