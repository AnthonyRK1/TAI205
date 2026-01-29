#1. importaciones
from fastapi import FastAPI

#3. Inicializaciones APP
app= FastAPI()

#4. Endpoints
@app.get("/")
async def holamundo():
    return {"mensage": "Hola mundo desde FastApi"}

@app.get("/")
async def bienvenidos():
    return {"mensage": "Bienvendios"}
