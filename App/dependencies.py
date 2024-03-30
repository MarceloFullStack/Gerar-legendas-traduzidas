from fastapi import Request, HTTPException, Security, Depends
from starlette.responses import JSONResponse
from config import KEYCLOAK_URL, REALM, CLIENT_ID, CLIENT_SECRET, TOKEN_URL
import requests
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

async def keycloak_auth_middleware(request: Request, call_next):
    # Exemplo para desproteger rotas especificas:
    if request.url.path in ["/login"]:  # Lista de rotas desprotegidas
        return await call_next(request)
    
    if "Authorization" not in request.headers:
        return JSONResponse(content={"detail": "Authorization header missing"}, status_code=401)

    auth_header = request.headers["Authorization"]
    try:
        token = auth_header.split(" ")[1]
    except IndexError:
        return JSONResponse(content={"detail": "Invalid Authorization header format"}, status_code=401)

    introspect_data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "token": token
    }
    response = requests.post(f"{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/token/introspect", data=introspect_data)
    if response.status_code != 200 or not response.json().get("active"):
        return JSONResponse(content={"detail": "Token is invalid or expired"}, status_code=401)

    return await call_next(request)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def validar_token(token: str = Security(oauth2_scheme)):
    introspect_url = f"{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/token/introspect"
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "token": token
    }
    response = requests.post(introspect_url, data=data)
    if response.status_code != 200 or not response.json().get("active"):
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")
    return response.json()

def login(form_data: OAuth2PasswordRequestForm = Depends()):
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "username": form_data.username,
        "password": form_data.password,
        "grant_type": "password",
    }    
    response = requests.post(TOKEN_URL, data=data)
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to login")