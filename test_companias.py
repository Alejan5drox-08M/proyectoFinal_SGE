import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Compania
from app.services.companias_services import CompaniasService

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

def test_delete_compania_by_id(db_session):
    """
    Prueba la eliminación de una compañía .
    """
    service = CompaniasService(db_session)

    # Crear una compañía de prueba
    compania = Compania(idcompania=1, nombrecompania="Test Airlines")
    db_session.add(compania)
    db_session.commit()

    # Verificar que la compañía existe antes de eliminarla
    assert db_session.query(Compania).filter_by(idcompania=1).first() is not None

    # Eliminar la compañía
    service.delete_compania_by_id(1)

    # Verificar que la compañía ha sido eliminada
    assert db_session.query(Compania).filter_by(idcompania=1).first() is None
