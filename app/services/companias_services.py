from fastapi.params import Depends
from sqlalchemy.orm import Session
from typing import List, Optional, Tuple, Any, Type
from app.models import Compania
from app.schemas import CompaniaCreate, CompaniaResponse
from app.db.database import get_db
class CompaniasService:
    def __init__(self, db: Session=Depends(get_db)):
        self.db = db

    def find_all(self) -> list[Type[Compania]]:
        return self.db.query(Compania).order_by(Compania.idcompania).all()

    def find_by_id(self, id: int) -> Optional[CompaniaResponse]:
        return self.db.query(Compania).filter(id == Compania.idcompania).first()

    def save_compania(self, compania_data: CompaniaCreate):
        compania = Compania(nombrecompania=compania_data.nombrecompania)
        self.db.add(compania)
        self.db.commit()
        self.db.refresh(compania)
        return compania
    def delete_compania_by_id(self, id: int):
        compania = self.db.query(Compania).filter(id == Compania.idcompania).first()
        if compania:
            self.db.delete(compania)
            self.db.commit()

    def cambiar_nombre(self, id: int, nombre_compania: str):
        compania = self.db.query(Compania).filter(id == Compania.idcompania).first()
        if compania:
            compania.nombrecompania = nombre_compania
            self.db.commit()
            self.db.refresh(compania)
