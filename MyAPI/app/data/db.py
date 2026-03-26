from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

#1. Definimos la URL de conexion con el contenedor
DATABASE_URL= os.getenv(
    "DATABASE_URL",
    "postgresql://admin:123456@postgres:5432/DB_miapi"
        
      
)

#2 Creamos motor de conexion 
engine= create_engine(DATABASE_URL)

#3. Definimos el manejador de sessiones
SessionLocal = sessionmaker(
    autocommit= False,
    autoflush= False,
    bind= engine
  
)

#4 Instaciamos la base declarativa del modelo
Base = declarative_base()

#5 funcion para manejo de sesiones por perticion

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    


