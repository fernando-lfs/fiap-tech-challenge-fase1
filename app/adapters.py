"""
Adapters para scraping e backup local.
"""
import requests
from bs4 import BeautifulSoup
import os
import json
import pandas as pd
from typing import List, Dict
from app.core.config import settings
import logging

BASE_URL = "http://vitibrasil.cnpuv.embrapa.br/index.php"

URLS = {
    "producao": "opt_02",
    "processamento": "opt_03",
    "comercializacao": "opt_04",
    "importacao": "opt_05",
    "exportacao": "opt_06"
}

def scrape_table(resource: str, ano: str) -> List[Dict]:
    """
    Raspagem da tabela do recurso especificado e ano.
    Extrai dados dos <td class="tb_item"> e <td class="tb_subitem">.
    Args:
        resource (str): Nome do recurso.
        ano (str): Ano para busca.
    Returns:
        List[Dict]: Dados raspados.
    Raises:
        Exception: Em caso de falha na raspagem.
    """
    params = {"ano": ano, "opcao": URLS[resource]}
    url = BASE_URL + f"?ano={ano}&opcao={URLS[resource]}"
    logging.info(f"[SCRAPER] URL requisitada: {BASE_URL} | Params: {params}")
    try:
        response = requests.get(BASE_URL, params=params, timeout=20)
        logging.info(f"[SCRAPER] Status code: {response.status_code}")
        response.raise_for_status()
        logging.debug(f"[SCRAPER] HTML início: {response.text[:300]}")
        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find("table", class_="tb_base tb_dados")
        if not table:
            logging.error(f"[SCRAPER] Tabela de dados não encontrada na página! URL: {url}")
            raise Exception("Tabela de dados não encontrada na página.")
        dados = []
        for tr in table.find_all("tr"):
            tds = tr.find_all("td")
            if len(tds) == 2:
                produto = tds[0].get_text(strip=True)
                quantidade = tds[1].get_text(strip=True)
                # Ignorar linhas totais e vazias
                if produto and produto.lower() != "total":
                    dados.append({"Produto": produto, "Quantidade (L.)": quantidade})
        logging.info(f"[SCRAPER] Produtos extraídos: {len(dados)}")
        if len(dados) == 0:
            logging.warning(f"[SCRAPER] Nenhum dado extraído da tabela! URL: {url}")
        logging.info(f"Scraping do recurso {resource} ano={ano} concluído com sucesso.")
        return dados
    except Exception as e:
        logging.error(f"Erro ao raspar {resource} ano={ano}: {e}")
        raise

def load_backup(resource: str, ano: str) -> List[Dict]:
    """
    Carrega backup local (CSV ou JSON) do recurso e ano.
    Args:
        resource (str): Nome do recurso.
        ano (str): Ano para filtro.
    Returns:
        List[Dict]: Dados do backup.
    Raises:
        Exception: Se não encontrar backup válido.
    """
    backup_dir = settings.backup_path
    csv_path = os.path.join(backup_dir, f"{resource}.csv")
    json_path = os.path.join(backup_dir, f"{resource}.json")
    logging.info(f"Tentando carregar backup local para {resource} ano={ano}")
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            filtrado = [row for row in data if any(str(row.get(k, "")).strip() == str(ano) for k in row.keys() if k.lower() == "ano")]
            logging.info(f"Backup JSON carregado para {resource} ano={ano}")
            return filtrado
    elif os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        filtrado = df[df.apply(lambda row: any(str(row[k]).strip() == str(ano) for k in row.index if k.lower() == "ano"), axis=1)]
        data = filtrado.to_dict(orient="records")
        logging.info(f"Backup CSV carregado para {resource} ano={ano}")
        return data
    else:
        logging.error(f"Backup local não encontrado para {resource} ano={ano}")
        raise FileNotFoundError(f"Backup local não encontrado para {resource} ano={ano}")
