from fastapi import status, HTTPException,Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

#seguridad HTTP BASIC
seguridad = HTTPBasic()
def verificar_peticion(credentials: HTTPBasicCredentials = Depends(seguridad)):
    userAuth = secrets.compare_digest(credentials.username, "Anthony")
    passAuth = secrets.compare_digest(credentials.password, "123")
    
    if not (userAuth and passAuth):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales no Autorizadas",
                  )
        return credenciales.username
    