from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://odoo:odoo@localhost:5342/fastapi_database"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine,autocommit=False,autoflush=False)
Base = declarative_base()

def get_db():
    db = SessionLocal() # Crear una nueva sesión
    try:
        yield db # Devuelve la sesión para su uso
    finally:
        db.close() # Cierra la sesión después de usarla