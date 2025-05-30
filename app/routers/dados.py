from fastapi import APIRouter, Depends, Query
from app.models.data import DataResponse
from app.services.scraping import get_resource_data
from app.core.security import verify_token

router_dados = APIRouter(prefix="/v1", tags=["Dados da Vitivinicultura"])

@router_dados.get("/producao", response_model=DataResponse)
def producao(
    ano: str = Query(default=None, description="Ano entre 1970 e 2023. Padrão: 2023"),
    user: dict = Depends(verify_token)
):
    """
    Retorna a produção de vinhos, sucos e derivados do Rio Grande do Sul.

    Em caso de filtro vazio ou data inválida, serão retornados dados do ano padrão configurado (2023).

    Returns:
        DataResponse: Dados de produção, ano efetivo, valor total e metadados.
    """
    return get_resource_data("producao", ano)

@router_dados.get("/processamento", response_model=DataResponse)
def processamento(
    ano: str = Query(default=None, description="Ano entre 1970 e 2023. Padrão: 2023"),
    user: dict = Depends(verify_token)
):
    """
    Retorna dados de processamento de uvas e derivados.

    Em caso de filtro vazio ou data inválida, serão retornados dados do ano padrão configurado (2023).

    Returns:
        DataResponse: Dados de processamento, ano efetivo, valor total e metadados.
    """
    return get_resource_data("processamento", ano)

@router_dados.get("/comercializacao", response_model=DataResponse)
def comercializacao(
    ano: str = Query(default=None, description="Ano entre 1970 e 2023. Padrão: 2023"),
    user: dict = Depends(verify_token)
):
    """
    Retorna dados de comercialização de vinhos e derivados.

    Em caso de filtro vazio ou data inválida, serão retornados dados do ano padrão configurado (2023).

    Returns:
        DataResponse: Dados de comercialização, ano efetivo, valor total e metadados.
    """
    return get_resource_data("comercializacao", ano)

@router_dados.get("/importacao", response_model=DataResponse)
def importacao(
    ano: str = Query(default=None, description="Ano entre 1970 e 2024. Padrão: 2024"),
    user: dict = Depends(verify_token)
):
    """
    Retorna dados de importação de vinhos e derivados por país.

    Em caso de filtro vazio ou data inválida, serão retornados dados do ano padrão configurado (2024).

    Returns:
        DataResponse: Dados de importação, ano efetivo, valor total e metadados.
    """
    return get_resource_data("importacao", ano)

@router_dados.get("/exportacao", response_model=DataResponse)
def exportacao(
    ano: str = Query(default=None, description="Ano entre 1970 e 2024. Padrão: 2024"),
    user: dict = Depends(verify_token)
):
    """
    Retorna dados de exportação de vinhos e derivados por país.

    Em caso de filtro vazio ou data inválida, serão retornados dados do ano padrão configurado (2024).

    Returns:
        DataResponse: Dados de exportação, ano efetivo, valor total e metadados.
    """
    return get_resource_data("exportacao", ano)

