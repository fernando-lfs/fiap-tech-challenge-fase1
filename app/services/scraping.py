from typing import Dict, Optional
from datetime import datetime
from app.adapters.embrapa_scraper import scrape_table
from app.adapters.local_backup import load_backup
import logging


def get_resource_data(resource: str, ano: Optional[str] = None) -> Dict:
    """
    Obter dados do recurso solicitado para o ano informado, via scraping online ou fallback local.
    Caso a requisição principal falhe (timeout, 404 ou 500), utiliza fallback local em arquivo JSON correspondente.

    Args:
        resource (str): Nome do recurso ('producao', 'processamento', etc).
        ano (str, opcional): Ano de referência.

    Returns:
        dict: Dados do recurso solicitado, incluindo fonte, timestamp, ano, valor_total e dados.

    Raises:
        HTTPException: Se ambos scraping e fallback local falharem.
    """
    """
    Obtém os dados do recurso solicitado para o ano informado, via scraping online ou fallback local.

    O fluxo é:
      1. Tenta scraping online do site da Embrapa para o recurso/ano.
      2. Se falhar, tenta carregar backup local (CSV/JSON) filtrado pelo ano.
      3. Se ambos falharem, retorna erro 503 amigável.

    O ano default é definido conforme o recurso:
      - 'importacao' e 'exportacao': ano default 2024
      - Demais recursos: ano default 2023
      - Se o ano for inválido ou não informado, utiliza o default.

    Os dados retornados pelo fallback local devem ser idênticos aos do scraping online, garantindo consistência (estrutura e tipos).

    Args:
        resource (str): Nome do recurso (producao, processamento, comercializacao, importacao, exportacao).
        ano (Optional[str]): Ano desejado. Se None ou inválido, aplica default conforme o recurso.

    Returns:
        dict: Resposta padronizada com as chaves:
            - fonte (str): 'online' ou 'local'.
            - timestamp (str): Data/hora da consulta (UTC, formato ISO8601).
            - ano (int): Ano efetivo dos dados.
            - valor_total (str): Valor total do recurso.
            - dados (list): Lista de registros conforme o recurso.

    Raises:
        HTTPException: 503 se dados indisponíveis online e local.
    """
    # Definir ano padrão por recurso
    if resource in ("importacao", "exportacao"):
        ano_padrao = "2024"
        ano_min, ano_max = 1970, 2024
    else:
        ano_padrao = "2023"
        ano_min, ano_max = 1970, 2023
    ano = str(ano) if ano else ano_padrao
    if not (ano.isdigit() and ano_min <= int(ano) <= ano_max):
        ano = ano_padrao
    try:
        resultado = scrape_table(resource, ano)
        fonte = "online"
    except Exception as e:
        logging.warning(f"[FALLBACK] Scraping falhou, tentando backup local: {e}")
        try:
            resultado = load_backup(resource, ano)
            fonte = "local"
        except Exception as e2:
            logging.error(f"[FALLBACK] Backup local também falhou: {e2}")
            from fastapi import HTTPException
            raise HTTPException(status_code=503, detail="Dados indisponíveis no momento (falha online e local).")
    # Monta o dicionário na ordem desejada, SEM OrderedDict
    resp = {
        "fonte": fonte,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "ano": resultado.get("ano"),
        "valor_total": resultado.get("valor_total", "-"),
        "dados": resultado.get("dados", [])
    }

    logging.info(f"Fonte dos dados de {resource}: {fonte}")
    return resp
