from fastapi import APIRouter, Depends, Query
from app.models.data import DataResponse
from app.services.scraping import get_resource_data
from app.core.security import verify_token

router_dados = APIRouter(prefix="/v1", tags=["Dados da Vitivinicultura"])

@router_dados.get(
    "/producao",
    response_model=DataResponse,
    summary="Obter dados de produção de vinhos, sucos e derivados",
    description=(
        "**Retornar dados de produção de vinhos, sucos e derivados do Rio Grande do Sul.**  \n\n"
        "Em caso de filtro vazio ou data inválida, serão retornados dados do ano padrão configurado.\n\n"
        "Caso a requisição principal falhe (timeout, 404 ou 500), utiliza fallback local em `producao.json`, retornando as informações do ano padrão configurado.\n\n"
        "**Parâmetros:**\n"
        "- `ano` (str, opcional): Ano de referência. Padrão: 2023.\n"
        "- `user` (dict): Usuário autenticado (extraído do JWT).\n\n"
        "**Retorno:**\n"
        "- `DataResponse`: Dados de produção, ano efetivo, valor total e metadados."
    )
)
def producao(
    ano: str = Query(default=None, description="Ano entre 1970 e 2023. Padrão: 2023"),
    user: dict = Depends(verify_token)
):
    """
    Retornar dados de produção de vinhos, sucos e derivados do RS.
    Caso a requisição principal falhe (timeout, 404 ou 500), utiliza fallback local em 'producao.json', retornando as informações do ano padrão configurado.

    Args:
        ano (str, opcional): Ano de referência. Padrão: 2023.
        user (dict): Usuário autenticado (extraído do JWT).

    Returns:
        DataResponse: Dados de produção, ano efetivo, valor total e metadados.
    """
    return get_resource_data("producao", ano)

@router_dados.get(
    "/processamento",
    response_model=DataResponse,
    summary="Obter dados de processamento de uvas",
    description=(
        "**Retornar dados de processamento de quantidade de uvas processadas no Rio Grande do Sul.**  \n"
        "**Obs.:** apenas viníferas.\n\n"
        "Em caso de filtro vazio ou data inválida, serão retornados dados do ano padrão configurado.\n\n"
        "Caso a requisição principal falhe (timeout, 404 ou 500), utiliza fallback local em `processamento.json`, retornando as informações do ano padrão configurado.\n\n"
        "**Parâmetros:**\n"
        "- `ano` (str, opcional): Ano de referência. Padrão: 2023.\n"
        "- `user` (dict): Usuário autenticado (extraído do JWT).\n\n"
        "**Retorno:**\n"
        "- `DataResponse`: Dados de processamento, ano efetivo, valor total e metadados."
    )
)
def processamento(
    ano: str = Query(default=None, description="Ano entre 1970 e 2023. Padrão: 2023"),
    user: dict = Depends(verify_token)
):
    """
    Retornar dados de processamento de uvas e derivados.
    Caso a requisição principal falhe (timeout, 404 ou 500), utiliza fallback local em 'processamento.json', retornando as informações do ano padrão configurado.

    Args:
        ano (str, opcional): Ano de referência. Padrão: 2023.
        user (dict): Usuário autenticado (extraído do JWT).

    Returns:
        DataResponse: Dados de processamento, ano efetivo, valor total e metadados.
    """
    return get_resource_data("processamento", ano)

@router_dados.get(
    "/comercializacao",
    response_model=DataResponse,
    summary="Obter dados de comercialização de vinhos",
    description=(
        "**Retornar dados de comercialização de vinhos e derivados no Rio Grande do Sul.**  \n\n"
        "Em caso de filtro vazio ou data inválida, serão retornados dados do ano padrão configurado.\n\n"
        "Caso a requisição principal falhe (timeout, 404 ou 500), utiliza fallback local em `comercializacao.json`, retornando as informações do ano padrão configurado.\n\n"
        "**Parâmetros:**\n"
        "- `ano` (str, opcional): Ano de referência. Padrão: 2023.\n"
        "- `user` (dict): Usuário autenticado (extraído do JWT).\n\n"
        "**Retorno:**\n"
        "- `DataResponse`: Dados de comercialização, ano efetivo, valor total e metadados."
    )
)
def comercializacao(
    ano: str = Query(default=None, description="Ano entre 1970 e 2023. Padrão: 2023"),
    user: dict = Depends(verify_token)
):
    """
    Retornar dados de comercialização de vinhos e derivados.
    Caso a requisição principal falhe (timeout, 404 ou 500), utiliza fallback local em 'comercializacao.json', retornando as informações do ano padrão configurado.

    Args:
        ano (str, opcional): Ano de referência. Padrão: 2023.
        user (dict): Usuário autenticado (extraído do JWT).

    Returns:
        DataResponse: Dados de comercialização, ano efetivo, valor total e metadados.
    """
    return get_resource_data("comercializacao", ano)

@router_dados.get(
    "/importacao",
    response_model=DataResponse,
    summary="Obter dados de importação de derivados de uva",
    description=(
        "**Retornar dados de importação de derivados de uva.**  \n"
        "**Obs.:** apenas vinhos de mesa.\n\n"
        "Em caso de filtro vazio ou data inválida, serão retornados dados do ano padrão configurado.\n\n"
        "Caso a requisição principal falhe (timeout, 404 ou 500), utiliza fallback local em `importacao.json`, retornando as informações do ano padrão configurado.\n\n"
        "**Parâmetros:**\n"
        "- `ano` (str, opcional): Ano de referência. Padrão: 2024.\n"
        "- `user` (dict): Usuário autenticado (extraído do JWT).\n\n"
        "**Retorno:**\n"
        "- `DataResponse`: Dados de importação, ano efetivo, valor total e metadados."
    )
)
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

@router_dados.get(
    "/exportacao",
    response_model=DataResponse,
    summary="Obter dados de exportação de derivados de uva",
    description=(
        "**Retornar dados de exportação de derivados de uva.**  \n"
        "**Obs.:** apenas vinhos de mesa.\n\n"
        "Em caso de filtro vazio ou data inválida, serão retornados dados do ano padrão configurado.\n\n"
        "Caso a requisição principal falhe (timeout, 404 ou 500), utiliza fallback local em `exportacao.json`, retornando as informações do ano padrão configurado.\n\n"
        "**Parâmetros:**\n"
        "- `ano` (str, opcional): Ano de referência. Padrão: 2024.\n"
        "- `user` (dict): Usuário autenticado (extraído do JWT).\n\n"
        "**Retorno:**\n"
        "- `DataResponse`: Dados de exportação, ano efetivo, valor total e metadados."
    )
)
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
