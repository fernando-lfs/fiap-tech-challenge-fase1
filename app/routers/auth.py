from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import UserCreate, UserOut
from app.models.auth import Token
from app.services.auth import add_user, authenticate_user
from app.core.security import create_access_token

router_auth = APIRouter(prefix="/v1/auth", tags=["Autenticação"])

@router_auth.post(
    "/cadastro",
    status_code=201,
    response_model=UserOut,
    summary="Cadastrar novo usuário",
    description=(
        "**Cadastrar um novo usuário na API.**  \n\n"
        "Cria um usuário persistente para autenticação futura. O nome de usuário deve ser único.\n\n"
        "**Parâmetros:**\n"
        "- `user` (UserCreate): Dados do usuário (username e password).\n\n"
        "**Retorno:**\n"
        "- `UserOut`: Dados públicos do usuário cadastrado.\n\n"
        "**Respostas de erro:**\n"
        "- 400: Usuário já existe."
    )
)
def cadastrar_usuario(user: UserCreate):
    """
    Cadastrar novo usuário na base persistente.

    Args:
        user (UserCreate): Dados do usuário a ser cadastrado.

    Returns:
        dict: Dados públicos do usuário cadastrado.

    Raises:
        HTTPException: Se o usuário já existir.
    """
    try:
        add_user(user.username, user.password)
        return {"username": user.username}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router_auth.post(
    "/login",
    response_model=Token,
    summary="Autenticar usuário e obter token JWT",
    description=(
        "**Autenticar usuário e gerar token JWT.**  \n\n"
        "Realiza a autenticação do usuário e retorna um token de acesso JWT para uso nos endpoints protegidos.\n\n"
        "**Parâmetros:**\n"
        "- `username` (str): Nome de usuário.\n"
        "- `password` (str): Senha do usuário.\n\n"
        "**Retorno:**\n"
        "- `Token`: Token JWT e tipo do token.\n\n"
        "**Respostas de erro:**\n"
        "- 401: Credenciais inválidas."
    )
)
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

