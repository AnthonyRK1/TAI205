from fastapi import status, HTTPException, Depends, APIRouter
from app.models.usuario import crear_usuario as CrearUsuario
from app.security.auth import verificar_peticion
from sqlalchemy.orm import Session
from app.data.db import get_db
from app.data.usuario import usuario as UsuarioDB


routerU = APIRouter(
    prefix="/v1/usuarios",
    tags=['CRUD HTTP']
)



@routerU.get("/")
async def leer_usuarios(db: Session = Depends(get_db)):
    queryUsuarios = db.query(UsuarioDB).all()
    return {
        "status": "200",
        "data": [{"id": u.id, "nombre": u.nombre, "edad": u.edad} for u in queryUsuarios],
        "total": len(queryUsuarios)
    }


@routerU.get("/total")
async def consultaT(db: Session = Depends(get_db)):
    queryUsuarios = db.query(UsuarioDB).all()
    return {
        "status": "200",
        "total": len(queryUsuarios),
        "data": [{"id": u.id, "nombre": u.nombre, "edad": u.edad} for u in queryUsuarios]
    }


@routerU.get("/{id}")
async def ConsultaUno(id: int, db: Session = Depends(get_db)):
    usuario = db.query(UsuarioDB).filter(UsuarioDB.id == id).first()
    if usuario:
        return {
            "Resultado": f"Usuario Encontrado: {usuario.nombre}",
            "Estatus": "200",
        }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Usuario no encontrado"
    )


@routerU.post("/")
async def crear_usuario(usuario: CrearUsuario, db: Session = Depends(get_db)):
    existente = db.query(UsuarioDB).filter(UsuarioDB.id == usuario.id).first()
    if existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El id ya existe"
        )
    nuevo = UsuarioDB(id=usuario.id, nombre=usuario.nombre, edad=usuario.edad)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return {
        "mensaje": "Usuario agregado correctamente",
        "status": "200",
        "usuario": {"id": nuevo.id, "nombre": nuevo.nombre, "edad": nuevo.edad}
    }


@routerU.put("/{id}")
async def actualizar_usuario(id: int, usuario: CrearUsuario, db: Session = Depends(get_db)):
    existente = db.query(UsuarioDB).filter(UsuarioDB.id == id).first()
    if not existente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    existente.nombre = usuario.nombre
    existente.edad = usuario.edad
    db.commit()
    db.refresh(existente)
    return {
        "mensaje": "Usuario actualizado",
        "usuario": {"id": existente.id, "nombre": existente.nombre, "edad": existente.edad}
    }


@routerU.delete("/{id}")
async def eliminar_usuario(id: int, db: Session = Depends(get_db), _: str = Depends(verificar_peticion)):
    existente = db.query(UsuarioDB).filter(UsuarioDB.id == id).first()
    if not existente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="no hay usuarios"
        )
    db.delete(existente)
    db.commit()
    return {
        "mensaje": "Usuario eliminado"
    }
