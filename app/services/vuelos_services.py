from fastapi.params import Depends
from sqlalchemy.orm import Session
from typing import List, Type
from app.models import Vuelo, Compania
from app.db.database import get_db
from app.schemas import VueloCreate


class VuelosService:
    def __init__(self, db: Session=Depends(get_db)):
        self.db = db

    def find_vuelos_by_origen_destino_numeroescalas(self, origen: str, destino: str, numeroescalas: int) -> list[Type[Vuelo]]:
        return self.db.query(Vuelo).filter(
            origen == Vuelo.origen,
            destino == Vuelo.destino,
            numeroescalas == Vuelo.numeroescalas
        ).all()

    def save_vuelo(self, vuelo_data: VueloCreate):
        nuevo_vuelo = Vuelo(
            idvuelo=vuelo_data.idvuelo,
            horasalida=vuelo_data.horasalida,
            origen=vuelo_data.origen,
            destino=vuelo_data.destino,
            precio=vuelo_data.precio,
            numeroescalas=vuelo_data.numeroescalas,
            idcompania=vuelo_data.idcompania
        )
        self.db.add(nuevo_vuelo)
        self.db.commit()
        self.db.refresh(nuevo_vuelo)
    def find_by_destino(self, destino: str) -> list[Type[Vuelo]]:
        return self.db.query(Vuelo).filter(destino == Vuelo.destino).all()

    def find_by_origen(self, origen: str) -> list[Type[Vuelo]]:
        return self.db.query(Vuelo).filter(origen == Vuelo.origen).all()

    def find_all(self) -> list[Type[Vuelo]]:
        return self.db.query(Vuelo).all()
