"""
Schemas Pydantic para respostas e autenticação.
"""
from typing import List, Any
from pydantic import BaseModel
from datetime import datetime

class Token(BaseModel):
    """Schema de resposta para token JWT."""
    access_token: str
    token_type: str

class DataResponse(BaseModel):
    """Schema padrão de resposta dos endpoints de dados."""
    fonte: str
    timestamp: datetime
    dados: List[Any]
