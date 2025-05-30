from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import UserCreate, UserOut
from app.models.auth import Token
from app.services.auth import add_user, authenticate_user
from app.core.security import create_access_token

router_auth = APIRouter(prefix="/v1/auth", tags=["Autenticação"])

@router_auth.post("/cadastro", status_code=201, response_model=UserOut)
def cadastrar_usuario(user: UserCreate):
    """Cadastra novo usuário (persistente)."""
    try:
        add_user(user.username, user.password)
        return {"username": user.username}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router_auth.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Autentica usuário e retorna JWT."""
    if not authenticate_user(form_data.username, form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha inválidos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token({"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}

