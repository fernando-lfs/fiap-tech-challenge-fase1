"""
Schemas Pydantic para autenticação, usuário e resposta de dados.
"""
from typing import List, Any
from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    username: str

class Token(BaseModel):
    access_token: str
    token_type: str

class DataResponse(BaseModel):
    fonte: str
    timestamp: datetime
    dados: List[Any]
