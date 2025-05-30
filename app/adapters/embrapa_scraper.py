import requests
from bs4 import BeautifulSoup
import logging
from typing import List, Dict

BASE_URL = "http://vitibrasil.cnpuv.embrapa.br/index.php"
URLS = {
    "producao": "opt_02",
    "processamento": "opt_03",
    "comercializacao": "opt_04",
    "importacao": "opt_05",
    "exportacao": "opt_06"
}

def scrape_table(resource: str, ano: str) -> dict:
    """
    Realiza a raspagem dos dados do site da Embrapa para o recurso e ano informados.
    Retorna dict com dados, valor_total (US$) e ano efetivo.
    - Para produção, processamento e comercialização: retorna lista de dicionários com Produto e Quantidade (L.).
    - Para importação e exportação: retorna lista de dicionários com País, Quantidade (Kg) e Valor (US$).
    - Intervalos disponíveis: produção/processamento/comercialização (1970-2023), importação/exportação (1970-2024).
    - Ano padrão conforme endpoint.
    - Retorna lista vazia se não houver dados para o ano.
    - valor_total (US$): string extraída da linha 'Total' da tabela.
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
        quantidade_total_kg = ""
        valor_total_usd = ""
        for tr in table.find_all("tr"):
            tds = tr.find_all("td")
            if resource in ("importacao", "exportacao"):
                # 3 colunas: Países, Quantidade (Kg), Valor (US$)
                if len(tds) == 3:
                    pais = tds[0].get_text(strip=True)
                    quantidade = tds[1].get_text(strip=True)
                    valor = tds[2].get_text(strip=True)
                    if pais and pais.lower() != "total":
                        dados.append({
                            "País": pais,
                            "Quantidade (Kg)": quantidade,
                            "Valor (US$)": valor
                        })
                    elif pais and pais.lower() == "total":
                        quantidade_total_kg = quantidade
                        valor_total_usd = valor
            else:
                # 2 colunas: Produto, Quantidade (L.)
                if len(tds) == 2:
                    produto = tds[0].get_text(strip=True)
                    quantidade = tds[1].get_text(strip=True)
                    if produto and produto.lower() != "total":
                        dados.append({"Produto": produto, "Quantidade (L.)": quantidade})
                    elif produto and produto.lower() == "total":
                        valor_total = quantidade
        logging.info(f"[SCRAPER] Linhas extraídas: {len(dados)} | Total (Kg): {quantidade_total_kg} | Valor total (US$): {valor_total_usd}")
        if len(dados) == 0:
            logging.warning(f"[SCRAPER] Nenhum dado extraído da tabela! URL: {url}")
        logging.info(f"Scraping do recurso {resource} ano={ano} concluído com sucesso.")
        return {"dados": dados, "valor_total": valor_total if valor_total else (quantidade_total_kg if quantidade_total_kg else valor_total_usd), "ano": int(ano)}
    except Exception as e:
        logging.error(f"Erro ao raspar {resource} ano={ano}: {e}")
        raise
