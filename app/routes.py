"""
Rotas da API: dados, autenticação, utilitários.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.models import DataResponse, Token, UserCreate, UserLogin, UserOut
from app.services import get_resource_data, add_user, authenticate_user, get_all_users, check_site_status
from app.core.security import create_access_token, verify_token, get_current_user

# Segmentos
router_dados = APIRouter(prefix="/v1", tags=["Dados da Vitivinicultura"])
router_auth = APIRouter(prefix="/v1/auth", tags=["Autenticação"])
router_utils = APIRouter(tags=["Utilitários"])

# Rotas de dados (GET)
@router_dados.get("/producao", response_model=DataResponse)
def producao(
    ano: str = Query(default=None, description="Ano para filtrar"),
    user: dict = Depends(verify_token)
):
    """Retorna dados de produção filtrados por ano (padrão 2024)."""
    return get_resource_data("producao", ano)

@router_dados.get("/processamento", response_model=DataResponse)
def processamento(
    ano: str = Query(default=None, description="Ano para filtrar"),
    user: dict = Depends(verify_token)
):
    """Retorna dados de processamento filtrados por ano (padrão 2024)."""
    return get_resource_data("processamento", ano)

@router_dados.get("/comercializacao", response_model=DataResponse)
def comercializacao(
    ano: str = Query(default=None, description="Ano para filtrar"),
    user: dict = Depends(verify_token)
):
    """Retorna dados de comercialização filtrados por ano (padrão 2024)."""
    return get_resource_data("comercializacao", ano)

@router_dados.get("/importacao", response_model=DataResponse)
def importacao(
    ano: str = Query(default=None, description="Ano para filtrar"),
    user: dict = Depends(verify_token)
):
    """Retorna dados de importação filtrados por ano (padrão 2024)."""
    return get_resource_data("importacao", ano)

@router_dados.get("/exportacao", response_model=DataResponse)
def exportacao(
    ano: str = Query(default=None, description="Ano para filtrar"),
    user: dict = Depends(verify_token)
):
    """Retorna dados de exportação filtrados por ano (padrão 2024)."""
    return get_resource_data("exportacao", ano)

# Rotas de autenticação
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
            detail="Usuário ou senha inválidos.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token({"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router_auth.get("/me", response_model=UserOut)
def usuario_logado(user: dict = Depends(get_current_user)):
    """Retorna o usuário autenticado."""
    return {"username": user["sub"]}

# Utilitários
