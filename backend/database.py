from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from enum import Enum as PyEnum

DATABASE_URL = "sqlite:///database.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Enums (si los necesitas aquí)
class EstadoUsuario(str, PyEnum):
    APROBADO = "Aprobado"
    RECHAZADO = "Rechazado"
    EN_REVISION = "En revisión"

class EstadoEntrega(str, PyEnum):
    PENDIENTE = "Pendiente"
    EN_CAMINO = "En camino"
    ENTREGADO = "Entregado"
    CANCELADO = "Cancelado"

# Función para poblar datos iniciales
def crear_datos():
    # [Mantén tu función actual tal como está]
    pass

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    crear_datos()