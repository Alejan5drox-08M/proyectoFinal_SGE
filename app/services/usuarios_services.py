import bcrypt
from sqlalchemy.orm import Session
from app.models import Usuario
from app.schemas import UsuarioCreate

class UsuariosService:
    def __init__(self, db: Session):
        self.db = db
    @staticmethod
    def hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def save_usuario(self, usuario_data: UsuarioCreate):
        # Verificar si el usuario ya existe
        usuario_existente = self.db.query(Usuario).filter(usuario_data.username == Usuario.username).first()
        if usuario_existente:
            raise ValueError("El usuario ya existe")

        # Crear nuevo usuario con contraseña hasheada
        nuevo_usuario = Usuario(
            username=usuario_data.username,
            password=self.hash_password(usuario_data.password)  # Hashear la contraseña
        )

        self.db.add(nuevo_usuario)
        self.db.commit()
        self.db.refresh(nuevo_usuario)

        return nuevo_usuario
