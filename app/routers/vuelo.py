from fastapi import APIRouter, HTTPException, Depends
from typing import List

from app.models import Compania
from app.schemas import VueloResponse, VueloCreate
from sqlalchemy.orm import Session
from app.services.vuelos_services import VuelosService
from app.db.database import get_db
router = APIRouter(prefix="/api/vuelos", tags=["Vuelos"])

@router.get("/", response_model=List[VueloResponse])
def get_all_vuelos(db: Session = Depends(get_db)):
    service=VuelosService(db)
    try:
        return service.find_all()
    except Exception:
        raise HTTPException(status_code=400, detail="Error al obtener todos los vuelos")

@router.post("/save")
def save_vuelo(vuelo_data: VueloCreate, db: Session = Depends(get_db)):
    service = VuelosService(db)
    compania = db.query(Compania).filter(Compania.idcompania == vuelo_data.idcompania).first()
    if not compania:
        raise HTTPException(status_code=400, detail="Compañía no encontrada")
    try:
        service.save_vuelo(vuelo_data)
        return "Vuelo guardado exitosamente"
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al guardar el vuelo{str(e)}")

@router.get("/origenydestinoynumeroescalas/{origen}/{destino}/{numeroescalas}", response_model=List[VueloResponse])
def get_by_origen_destino_numeroescalas(origen: str, destino: str, numeroescalas: int, db: Session = Depends(get_db)):
    service = VuelosService(db)
    try:
        return service.find_vuelos_by_origen_destino_numeroescalas(origen, destino, numeroescalas)
    except Exception:
        raise HTTPException(status_code=400, detail="Error al obtener vuelos por los filtros citados")

@router.get("/destino/{destino}", response_model=List[VueloResponse])
def get_by_destino(destino: str, db: Session = Depends(get_db)):
    service = VuelosService(db)
    try:
        return service.find_by_destino(destino)
    except Exception:
        raise HTTPException(status_code=400, detail="Error al obtener vuelos por destino")

@router.get("/origen/{origen}", response_model=List[VueloResponse])
def get_by_origen(origen: str, db: Session = Depends(get_db)):
    service = VuelosService(db)
    try:
        return service.find_by_origen(origen)
    except Exception:
        raise HTTPException(status_code=400, detail="Error al obtener vuelos por origen")
