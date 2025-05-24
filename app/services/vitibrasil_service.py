"""
Serviço de orquestração: tenta scraping, faz fallback para backup local.
"""
from datetime import datetime
from typing import List, Any, Dict
from app.adapters.scraper import scrape_table
from app.adapters.backup import load_backup
import logging


def get_resource_data(resource: str) -> Dict:
    """
    Orquestra obtenção de dados: tenta scraping, faz fallback para backup local.
    Args:
        resource (str): Nome do recurso.
    Returns:
        Dict: Dicionário com fonte, timestamp e dados.
    """
    try:
        dados = scrape_table(resource)
        fonte = "online"
    except Exception:
        dados = load_backup(resource)
        fonte = "local"
    resp = {
        "fonte": fonte,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "dados": dados
    }
    logging.info(f"Fonte dos dados de {resource}: {fonte}")
    return resp
