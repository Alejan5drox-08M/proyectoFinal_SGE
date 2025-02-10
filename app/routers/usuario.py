from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Usuario
from app.schemas import UsuarioCreate
from app.services.usuarios_services import UsuariosService
from app.db.database import get_db

router = APIRouter(prefix="/api/usuarios", tags=["Usuarios"])

@router.post("/usuarios/create", response_model=dict)
def create_usuario(usuario_data: UsuarioCreate, db: Session = Depends(get_db)):
    service = UsuariosService(db)


    usuario_existente = db.query(Usuario).filter(usuario_data.username == Usuario.username).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="El usuario ya existe")

    try:
        service.save_usuario(usuario_data)
        return {"message": "Usuario creado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error al crear usuario: {str(e)}")
