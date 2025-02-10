from pydantic import BaseModel, Field
from typing import List


class VueloBase(BaseModel):
    idvuelo: str = Field(..., max_length=10)
    horasalida: str = Field(..., max_length=50)
    origen: str = Field(..., max_length=50)
    destino: str = Field(..., max_length=50)
    precio: float
    numeroescalas: int
    idcompania: int


class VueloCreate(VueloBase):
    pass


class VueloResponse(VueloBase):
    model_config = {
        "from_attributes": True
    }

class CompaniaBase(BaseModel):
    nombrecompania: str = Field(..., max_length=50)


class CompaniaCreate(CompaniaBase):
    pass


class CompaniaResponse(CompaniaBase):
    idcompania: int
    vuelos: List[VueloResponse]

    model_config = {
        "from_attributes":True
    }

class UsuarioBase(BaseModel):
    username: str = Field(..., max_length=255)


class UsuarioCreate(UsuarioBase):
    password: str = Field(..., max_length=255)


class UsuarioResponse(UsuarioBase):
    model_config = {
        "from_attributes": True
    }

