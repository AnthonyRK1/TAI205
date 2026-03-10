from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import date, datetime

app = FastAPI()
security = HTTPBasic()

class Reserva(BaseModel):
    nombre: str = Field(..., min_length=5, max_length=100)
    email: str = Field(..., min_length=5)
    tipo_habitacion: str = Field(...)
    fechaEntrada: str = Field(...)
    fechaSalida: str = Field(...)
    huespedes: int = Field(..., gt=0, lt=10)

    @validator("tipo_habitacion")
    def tipo_valido(cls, v):
        if v not in ["sencilla", "doble", "suite"]:
            raise ValueError("tipo de habitacion invalido")
        return v

    @validator("fechaEntrada", "fechaSalida")
    def formato_fecha(cls, v):
        try:
            datetime.fromisoformat(v)
        except Exception:
            raise ValueError("La fecha no es valida porfa usa esta estructura YYYY-MM-DD")
        return v

    @validator("fechaSalida")
    def salida_mayor_entrada(cls, v, values):
        if "fechaEntrada" not in values:
            return v
        entrada = datetime.fromisoformat(values["fechaEntrada"]).date()
        salida = datetime.fromisoformat(v).date()
        if salida <= entrada:
            raise ValueError("la fecha de salida debe ser mayor que la fecha entrada")
        if (salida - entrada).days > 7:
            raise ValueError("la estancia de la o las personas no puede ser mayor a 7 dias")
        return v

    @validator("fechaEntrada")
    def entrada_no_menor_actual(cls, v):
        entrada = datetime.fromisoformat(v).date()
        if entrada < date.today():
            raise ValueError("la fecha de entrada no puede ser menor a la fecha actual")
        return v

reservas_db: List[dict] = []
id_counter = 1

def autenticar(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != "hotel" or credentials.password != "r2026":
        raise HTTPException(status_code=401, detail="No estas autorizado para  hacer esta accion")

@app.post("/reservas", status_code=201)
def crear_reserva(reserva: Reserva, auth: None = Depends(autenticar)):
    global id_counter
    for r in reservas_db:
        if r["email"] == reserva.email:
            raise HTTPException(status_code=409, detail="este email, ya fue registrado usa otro")
    nueva_reserva = reserva.dict()
    nueva_reserva["id"] = id_counter
    nueva_reserva["estado"] = "pendiente"
    id_counter += 1
    reservas_db.append(nueva_reserva)
    return nueva_reserva

@app.get("/reservas", status_code=200)
def listar_reservas():
    return reservas_db

@app.get("/reservas/{reserva_id}", status_code=200)
def consultar_reserva(reserva_id: int):
    for reserva in reservas_db:
        if reserva["id"] == reserva_id:
            return reserva
    raise HTTPException(status_code=404, detail="La reserva no ha sido encontrada en el registro")

@app.patch("/reservas/{reserva_id}/confirmar", status_code=200)
def confirmar_reserva(reserva_id: int):
    for reserva in reservas_db:
        if reserva["id"] == reserva_id:
            if reserva["estado"] == "confirmada":
                raise HTTPException(status_code=409, detail="La reservacion esta confirmada por el hotel")
            reserva["estado"] = "confirmada"
            return reserva
    raise HTTPException(status_code=404, detail="Esta reserva no se encontro en el registro")

@app.patch("/reservas/{reserva_id}/cancelar", status_code=200)
def cancelar_reserva(reserva_id: int, auth: None = Depends(autenticar)):
    for reserva in reservas_db:
        if reserva["id"] == reserva_id:
            if reserva["estado"] == "cancelada":
                raise HTTPException(status_code=409, detail="La reserva fue cancelada por el hotel")
            reserva["estado"] = "cancelada"
            return reserva
    raise HTTPException(status_code=404, detail="La reserva no esta en el regitro ")








































































































