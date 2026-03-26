from fastapi import FastAPI
from app.routers import usuario as usuario_router, varios
from app.data.db import engine, Base
import app.data.usuario  # registra el modelo antes de create_all


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title='Mi primera API con FastApi',
    description="Anthony Ramos",
    version="1.0.0"
)

app.include_router(usuario_router.routerU)
app.include_router(varios.routerV)
