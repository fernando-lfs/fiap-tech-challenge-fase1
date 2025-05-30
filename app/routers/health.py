from fastapi import APIRouter
from app.services.utils import check_site_status

router_utils = APIRouter(tags=["Utilitários"])

@router_utils.get("/health", summary="Teste de saúde da API")
def health_check():
    """
    Retorna o status do servidor FastAPI e do site da Embrapa.
    - "api": sempre "online" se o servidor está respondendo.
    - "site_embrapa": "online" se o site está acessível, "offline" caso contrário.
    """
    status_embrapa = "online" if check_site_status() else "offline"
    return {
        "api": "online",
        "site_embrapa": status_embrapa
    }

