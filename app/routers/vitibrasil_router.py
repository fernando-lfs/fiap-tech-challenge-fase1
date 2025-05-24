"""
Rotas protegidas para recursos do Vitibrasil.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from app.services.vitibrasil_service import get_resource_data
from app.models.schemas import DataResponse, Token
from app.core.security import verify_token, create_access_token, FAKE_USER
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/v1", tags=["Vitibrasil"])

@router.post("/token", response_model=Token, tags=["auth"])
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Endpoint para autenticação e geração de token JWT.
    """
    if (form_data.username == FAKE_USER["username"] and
            form_data.password == FAKE_USER["password"]):
        access_token = create_access_token({"sub": form_data.username})
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Usuário ou senha inválidos.",
        headers={"WWW-Authenticate": "Bearer"},
    )

@router.get("/producao", response_model=DataResponse)
def producao(token: dict = Depends(verify_token)):
    """Retorna dados de produção."""
    return get_resource_data("producao")

@router.get("/processamento", response_model=DataResponse)
def processamento(token: dict = Depends(verify_token)):
    """Retorna dados de processamento."""
    return get_resource_data("processamento")

@router.get("/comercializacao", response_model=DataResponse)
def comercializacao(token: dict = Depends(verify_token)):
    """Retorna dados de comercialização."""
    return get_resource_data("comercializacao")

@router.get("/importacao", response_model=DataResponse)
def importacao(token: dict = Depends(verify_token)):
    """Retorna dados de importação."""
    return get_resource_data("importacao")

@router.get("/exportacao", response_model=DataResponse)
def exportacao(token: dict = Depends(verify_token)):
    """Retorna dados de exportação."""
    return get_resource_data("exportacao")
