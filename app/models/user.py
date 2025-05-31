# Schemas e modelos relacionados a usuários
from pydantic import BaseModel

class UserCreate(BaseModel):
    """
    Modelo para criação de novo usuário.

    Attributes:
        username (str): Nome de usuário.
        password (str): Senha do usuário.
    """
    username: str
    password: str

class UserLogin(BaseModel):
    """
    Modelo para autenticação de usuário.

    Attributes:
        username (str): Nome de usuário.
        password (str): Senha do usuário.
    """
    username: str
    password: str

class UserOut(BaseModel):
    """
    Modelo de saída de usuário (apresentação).

    Attributes:
        username (str): Nome de usuário.
    """
    username: str
