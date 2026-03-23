# 1. Importaciones
from fastapi import FastAPI, status, HTTPException, Depends
from typing import Optional
import asyncio
from pydantic import BaseModel, Field
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
import jwt

# 2. Configuración JWT
SECRET_KEY = "mi_clave_super_secreta_12345"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1

# 3. Inicialización APP
app = FastAPI(
    title='Mi primera API con FastAPI',
    description="Anthony Ramos",
    version="1.0.0"
)

# Base de datos ficticia de usuarios CRUD
usuarios = [
    {"id": 1, "nombre": "Anthony", "edad": 20},
    {"id": 2, "nombre": "Berni", "edad": 20},
    {"id": 3, "nombre": "Marco", "edad": 24},
]

# Base de datos ficticia de autenticación
usuarios_sistema = {
    "Anthony": {
        "username": "Anthony",
        "password": "123"
    }
}

# Modelo de validación de Pydantic
class UsuarioCrear(BaseModel):
    id: int = Field(..., gt=0, description="Identificador de usuario")
    nombre: str = Field(..., min_length=3, max_length=50, example="Juan")
    edad: int = Field(..., ge=1, le=123, description="Edad válida entre 1 y 123")

class Token(BaseModel):
    access_token: str
    token_type: str

# OAuth2 esquema
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 4. Funciones JWT
def crear_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verificar_token(token: str = Depends(oauth2_scheme)):
    credenciales_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No autorizado. Token inválido, expirado o ausente",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise credenciales_exception

        return username

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="El token ha expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise credenciales_exception

# 5. Endpoint para generar token
@app.post("/token", response_model=Token, tags=["Autenticación"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    usuario = usuarios_sistema.get(form_data.username)

    if not usuario or usuario["password"] != form_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = crear_token(
        data={"sub": usuario["username"]},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

# 6. Endpoints
@app.get("/", tags=['Inicio'])
async def hola_mundo():
    return {"mensaje": "Hola mundo desde FastAPI"}

@app.get("/v1/bienvenidos", tags=['Inicio'])
async def bienvenidos():
    return {"mensaje": "Bienvenidos"}

@app.get("/v1/promedio", tags=['Calificaciones'])
async def promedio():
    await asyncio.sleep(2)
    return {
        "Calificacion": "7",
        "estatus": 200
    }

@app.get("/v1/usuario/{id}", tags=['Parámetros'])
async def consulta_uno(id: int):
    await asyncio.sleep(2)

    usuario = next((usr for usr in usuarios if usr["id"] == id), None)
    if usuario:
        return {
            "Resultado": f"Usuario Encontrado: {usuario['nombre']}",
            "Estatus": "200",
        }
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@app.get("/v1/usuarios", tags=['CRUD HTTP'])
async def consulta_todos():
    return {
        "status": "200",
        "total": len(usuarios),
        "data": usuarios
    }

@app.post("/v1/usuarios", tags=['CRUD HTTP'])
async def crear_usuario(usuario: UsuarioCrear):
    if any(usr["id"] == usuario.id for usr in usuarios):
        raise HTTPException(
            status_code=400,
            detail="El id ya existe"
        )

    usuarios.append(usuario.dict())

    return {
        "mensaje": "Usuario agregado correctamente",
        "status": "200",
        "usuario": usuario
    }

# PROTEGIDO CON JWT
@app.put("/v1/usuarios/{id}", tags=['CRUD HTTP'])
async def actualizar_usuario(
    id: int,
    usuario: dict,
    user_auth: str = Depends(verificar_token)
):
    for usr in usuarios:
        if usr["id"] == id:
            usr.update(usuario)
            return {
                "mensaje": f"Usuario actualizado por {user_auth}",
                "usuario": usr
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )

# PROTEGIDO CON JWT
@app.delete("/v1/usuarios/{id}", tags=['CRUD HTTP'])
async def eliminar_usuario(
    id: int,
    user_auth: str = Depends(verificar_token)
):
    for usr in usuarios:
        if usr["id"] == id:
            usuarios.remove(usr)
            return {
                "mensaje": f"Usuario eliminado por {user_auth}"
            }

    raise HTTPException(status_code=404, detail="No hay usuarios")