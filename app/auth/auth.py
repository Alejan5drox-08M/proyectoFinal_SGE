import hashlib

import bcrypt
from sqlalchemy import and_

from sqlalchemy.orm import Session
from app.models import Usuario
from app.db.database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
import os

router = APIRouter(prefix="/api", tags=["Token Control"])


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")

SECRET_KEY = os.getenv("SECRET_KEY", "clave_super_secreta")
ALGORITHM = "HS256"

def create_token(data: dict):
    """Genera un token JWT."""
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Autenticación de usuario y generación de token."""
    usuario = db.query(Usuario).filter(form_data.username == Usuario.username).first()

    if not usuario:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    if not bcrypt.checkpw(form_data.password.encode(), usuario.password.encode()):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    token = create_token(data={"sub": usuario.username})
    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.get("/getToken")
def get_token(token: str = Depends(oauth2_scheme)):
    """Decodifica el token JWT y retorna la información del usuario."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if not username:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
        return {"username": username}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expirado")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

