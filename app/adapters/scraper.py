"""
Funções de scraping para cada recurso do Vitibrasil.
"""
import requests
from bs4 import BeautifulSoup
import logging
from typing import List, Any

BASE_URL = "http://vitibrasil.cnpuv.embrapa.br/index.php?opcao="

URLS = {
    "producao": "opt_02",
    "processamento": "opt_03",
    "comercializacao": "opt_04",
    "importacao": "opt_05",
    "exportacao": "opt_06"
}

def scrape_table(resource: str) -> List[Any]:
    """
    Raspagem da tabela do recurso especificado.
    Args:
        resource (str): Nome do recurso.
    Returns:
        List[Any]: Dados raspados.
    Raises:
        Exception: Em caso de falha na raspagem.
    """
    url = BASE_URL + URLS[resource]
    logging.info(f"Iniciando scraping do recurso {resource} em {url}")
    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find("table")
        if not table:
            raise Exception("Tabela não encontrada na página.")
        headers = [th.get_text(strip=True) for th in table.find_all("th")]
        rows = []
        for tr in table.find_all("tr")[1:]:
            cells = [td.get_text(strip=True) for td in tr.find_all(["td", "th"])]
            if cells:
                rows.append(dict(zip(headers, cells)))
        logging.info(f"Scraping do recurso {resource} concluído com sucesso.")
        return rows
    except Exception as e:
        logging.error(f"Erro ao raspar {resource}: {e}")
        raise
