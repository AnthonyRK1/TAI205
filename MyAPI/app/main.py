from fastapi import FastAPI 
from app.routers import usuario,varios

app = FastAPI(
    title='Mi primera API con FastApi',
    description="Anthony Ramos",
    version="1.0.0"
)

app.include_router(usuario.routerU)
app.include_router(varios.routerV)




    
    
    

   