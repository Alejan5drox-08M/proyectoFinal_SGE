from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session

from app.auth import auth
from app.schemas import CompaniaResponse, CompaniaCreate
from app.services.companias_services import CompaniasService
from app.db.database import get_db

router = APIRouter(prefix="/api/companias", tags=["Compañias"])

@router.get("/", response_model=List[CompaniaResponse])
def get_all_companias(db: Session=Depends(get_db), token:str = Depends(auth.oauth2_scheme)):
    service=CompaniasService(db)
    try:
        return service.find_all()
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error al obtener todas las compañias")

@router.post("/save")
def save_compania(compania: CompaniaCreate, db: Session = Depends(get_db), token:str = Depends(auth.oauth2_scheme)):
    service = CompaniasService(db)
    try:
        service.save_compania(compania)
        return "Compañia insertada correctamente"
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error al guardar la nueva compañia")

@router.delete("/delete/{id}")
def delete_compania(id: int, db: Session = Depends(get_db), token:str = Depends(auth.oauth2_scheme)):
    service = CompaniasService(db)
    try:
        compania=service.find_by_id(id)
        if not compania:
            raise HTTPException(status_code=404, detail="No se encontró la compañia")
        else:
            service.delete_compania_by_id(id)
            return "Compañia eliminada correctamente"
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error al eliminar la compañia por ID")

@router.put("/edit/{id}/{nombre}")
def edit_compania(id: int, nombre: str, db: Session = Depends(get_db), token:str = Depends(auth.oauth2_scheme)):
    service = CompaniasService(db)
    try:
        compania = service.find_by_id(id)
        if compania:
            raise HTTPException(status_code=404, detail="No se encontró la compañia")
        else:
            service.cambiar_nombre(id, nombre)
            return "Nombre de compañia editado correctamente"

    except Exception as e:
        raise HTTPException(status_code=400, detail="Error al editar la compañia")
