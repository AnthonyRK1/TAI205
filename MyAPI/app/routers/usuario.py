from fastapi import status, HTTPException, Depends, APIRouter
from app.data.database import usuarios
from app.models.usuario import crear_usuario as CrearUsuario
from app.security.auth import verificar_peticion
import asyncio

routerU = APIRouter(
    prefix="/v1/usuarios",
    tags=['CRUD HTTP']
)

@routerU.get("/")
async def leer_usuarios():
    return {
        "status": "200",
        "data": usuarios,
        "total": len(usuarios)
    }


@routerU.get("/total")
async def consultaT():
    return {
        "status": "200",
        "total": len(usuarios),
        "data": usuarios
    }


@routerU.get("/{id}")
async def ConsultaUno(id: int):
    await asyncio.sleep(2)

    usuario = next((usr for usr in usuarios if usr["id"] == id), None)
    if usuario:
        return {
            "Resultado": f"Usuario Encontrado: {usuario['nombre']}",
            "Estatus": "200",
        }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Usuario no encontrado"
    )


@routerU.post("/")
async def crear_usuario(usuario: CrearUsuario):
    if any(usr["id"] == usuario.id for usr in usuarios):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El id ya existe"
        )

    usuarios.append(usuario.dict())

    return {
        "mensaje": "Usuario agregado correctamente",
        "status": "200",
        "usuario": usuario
    }


@routerU.put("/{id}")
async def actualizar_usuario(id: int, usuario: dict):
    for usr in usuarios:
        if usr["id"] == id:
            usr.update(usuario)
            return {
                "mensaje": "Usuario actualizado",
                "usuario": usr
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Usuario no encontrado"
    )


@routerU.delete("/{id}")
async def eliminar_usuario(id: int, userAuth: str = Depends(verificar_peticion)):
    for usr in usuarios:
        if usr["id"] == id:
            usuarios.remove(usr)
            return {
                "mensaje": "Usuario eliminado por Anthony"
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="no hay usuarios"
    )