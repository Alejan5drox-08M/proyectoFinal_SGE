from fastapi import FastAPI
import uvicorn

from app.routers import compania,vuelo,usuario
from app.auth import auth
from app.db.database import Base, engine

def create_tables():
    Base.metadata.create_all(bind=engine)

create_tables()



app= FastAPI()
app.include_router(compania.router)
app.include_router(vuelo.router)
app.include_router(usuario.router)
app.include_router(auth.router)
if __name__=="__main__":

    uvicorn.run("main:app",port=8000,reload=True)


