from typing import List, Any
from pydantic import BaseModel
from datetime import datetime

class DataResponse(BaseModel):
    """
    Modelo de resposta para dados dos endpoints da API.

    Attributes:
        fonte (str): Origem dos dados ('online' ou 'local').
        timestamp (datetime): Data/hora da resposta.
        ano (int): Ano efetivamente filtrado/retornado.
        valor_total (str): Valor total extraído da tabela.
        dados (List[Any]): Lista de registros extraídos.
    """
    fonte: str
    timestamp: datetime
    ano: int
    valor_total: str
    dados: List[Any]

    class Config:
        json_schema_extra = {
            "example": {
                "fonte": "online",
                "timestamp": "2025-05-30T00:00:00Z",
                "ano": 2024,
                "valor_total": "457.792.870",
                "dados": []
            }
        }


