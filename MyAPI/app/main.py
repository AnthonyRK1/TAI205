#1. Importaciones
from fastapi import FastAPI, status, HTTPException
from typing import Optional
import asyncio
from pydantic import BaseModel, Field

#3. Inicializaciones APP
app = FastAPI(
    title='Mi primera API con FastApi',
    description="Anthony Ramos",
    version="1.0.0"
)

#Base de datos ficticia
usuarios = [
    {"id": 1, "nombre": "Anthony", "edad": 20},
    {"id": 2, "nombre": "berni", "edad": 20},
    {"id": 3, "nombre": "Marco", "edad": 24},
]

# Modelo de Validacion de pydantic
class crear_usuario(BaseModel):
    id: int = Field(...,gt=0, description="Identificar de usuario")
    nombre: str= Field(..., min_length=3, max_length=50,example="juata")
    edad: int= Field(...,ge=1,le=123,description="Edad valida entre 1 y 123")

#4. Endpoints
@app.get("/", tags=['Inicio'])
async def holaMundo():
    return {"mensaje": "Hola mundo desde FastApi"}

@app.get("/v1/bienvenidos", tags=['Inicio'])
async def bienvenidos():
    return {"mensaje": "Bienvenidos"}

@app.get("/v1/promedio", tags=['Calificaciones'])
async def promedio():
    await asyncio.sleep(2)  # Simulando una operación asíncrona
    return {
        "Calificacion": "7",
        "estatus": 200
    }

@app.get("/v1/usuario/{id}", tags=['Parametros'])
async def ConsultaUno(id: int):
    await asyncio.sleep(2)

    usuario = next((usr for usr in usuarios if usr["id"] == id), None)
    if usuario:
        return {
            "Resultado": f"Usuario Encontrado: {usuario['nombre']}",
            "Estatus": "200",
        }
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@app.get("/v1/usuarios", tags=['CRUD HTTP'])
async def consultaT():
    return {
        "status": "200",
        "total": len(usuarios),
        "data": usuarios
    }

@app.post("/v1/usuarios", tags=['CRUD HTTP'])
async def crear_usuario(usuario: crear_usuario):
    # Verificar si ya existe un usuario con el mismo id
    if any(usr["id"] == usuario.id for usr in usuarios):
        raise HTTPException(
            status_code=400,
            detail="El id ya existe"
        )

    # ✅ guardar como dict (no como objeto pydantic)
    usuarios.append(usuario.dict())

    return {
        "mensaje": "Usuario agregado correctamente",
        "status": "200",
        "usuario": usuario
    }

@app.put("/v1/usuarios/{id}", tags=['CRUD HTTP'])
async def actualizar_usuario(id: int, usuario: dict):
    for usr in usuarios:
        if usr["id"] == id:
            usr.update(usuario)
            return {
                "mensaje": "Usuario actualizado",
                "usuario": usr
            }
    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )

@app.delete("/v1/usuarios/{id}", tags=['CRUD HTTP'])
async def eliminar_usuario(id: int):
    for usr in usuarios:
        if usr["id"] == id:
            usuarios.remove(usr)
            return {
                "mensaje": "Usuario eliminado"
            }
    raise HTTPException(status_code=404, detail="no hay usuarios")



    
    
    
    

   