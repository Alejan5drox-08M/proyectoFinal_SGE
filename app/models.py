from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base


class Compania(Base):
    __tablename__ = "companias"
    idcompania = Column(Integer, primary_key=True, autoincrement=True)
    nombrecompania = Column(String(50), nullable=False)
    vuelos = relationship("Vuelo", backref="compania", cascade="all, delete-orphan")

class Vuelo(Base):
    __tablename__ = "vuelos"
    idvuelo = Column(String(10), primary_key=True)
    horasalida = Column(String(50), nullable=False)
    origen = Column(String(50), nullable=False)
    destino = Column(String(50), nullable=False)
    precio = Column(Float, nullable=False)
    numeroescalas = Column(Integer, nullable=False)
    idcompania = Column(Integer, ForeignKey("companias.idcompania", ondelete="CASCADE"))

class Usuario(Base):
    __tablename__ = "usuarios"
    username = Column(String(255), primary_key=True)
    password = Column(String(255), nullable=False)
