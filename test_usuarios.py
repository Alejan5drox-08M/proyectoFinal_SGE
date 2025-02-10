import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Usuario
from app.schemas import UsuarioCreate
from app.services.usuarios_services import UsuariosService

# Configurar una base de datos en memoria para pruebas
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """
    Crea una sesión de base de datos en memoria para las pruebas.
    """
    Base.metadata.create_all(bind=engine)  # Crear las tablas en memoria
    db = TestingSessionLocal()
    yield db  # Proveer la sesión para el test
    db.close()
    Base.metadata.drop_all(bind=engine)  # Eliminar tablas después de la prueba


def test_save_usuario(db_session):
    """
    Prueba la creación de un usuario en UsuariosService.
    """
    service = UsuariosService(db_session)

    usuario_data = UsuarioCreate(username="test_user", password="securepassword")

    nuevo_usuario = service.save_usuario(usuario_data)

    # Verificar que el usuario se ha guardado correctamente
    assert nuevo_usuario.username == "test_user"
    assert nuevo_usuario.password is not None

    # Verificar que la contraseña está hasheada
    assert nuevo_usuario.password != "securepassword"  # No debe ser la misma que la original
