import os
import json
import pandas as pd
from typing import List, Dict
from app.core.config import settings
import logging

def load_backup(resource: str, ano: str) -> dict:
    """
    Carrega backup local (CSV ou JSON) do recurso e ano, para fallback em caso de falha no scraping online.

    O arquivo local deve conter dados equivalentes aos do scraping online, garantindo consistência na estrutura e tipos de dados.
    O ano default é definido conforme o recurso (2024 para importacao/exportacao, 2023 para demais).

    Args:
        resource (str): Nome do recurso (producao, processamento, comercializacao, importacao, exportacao).
        ano (str): Ano para filtro. Deve ser coerente com o ano default do recurso.

    Returns:
        dict: Estrutura padronizada com as chaves:
            - dados (list): Lista de registros do recurso.
            - valor_total (str): Valor total do recurso.
            - ano (int): Ano efetivo dos dados.

    Raises:
        Exception: Se não encontrar backup válido ou dados para o ano solicitado.
    """
    backup_dir = settings.backup_path
    csv_path = os.path.join(backup_dir, f"{resource}.csv")
    json_path = os.path.join(backup_dir, f"{resource}.json")
    logging.info(f"Tentando carregar backup local para {resource} ano={ano}")
    # Definir ano default conforme recurso
    if resource in ("importacao", "exportacao"):
        ano_default = "2024"
    else:
        ano_default = "2023"

    dados = []
    ano_efetivo = ano
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Novo formato: dicionário com campos fonte, timestamp, ano, valor_total (US$), dados
            if isinstance(data, dict) and "dados" in data:
                # Se ano não bater, tenta ano default
                if str(data.get("ano")) != str(ano):
                    if str(data.get("ano")) == str(ano_default):
                        ano_efetivo = ano_default
                    else:
                        raise Exception(f"Backup local não possui dados para o ano solicitado nem para o default: {ano}/{ano_default}")
                dados = data["dados"]
                total = data.get("valor_total", data.get("valor_total (US$)", data.get("quantidade_total (L.)", data.get("quantidade_total (Kg)", "-"))))
                fonte = data.get("fonte", "local")
                timestamp = data.get("timestamp")
                return {
                    "fonte": fonte,
                    "timestamp": timestamp,
                    "ano": int(ano_efetivo),
                    "valor_total": total,
                    "dados": dados
                }
            # Formato antigo: lista direta
            elif isinstance(data, list):
                dados = [row for row in data if any(str(row.get(k, "")).strip() == str(ano) for k in row.keys() if k.lower() == "ano")]
                if not dados and ano != ano_default:
                    # Tenta ano default
                    dados = [row for row in data if any(str(row.get(k, "")).strip() == str(ano_default) for k in row.keys() if k.lower() == "ano")]
                    if dados:
                        ano_efetivo = ano_default
                logging.info(f"Backup JSON carregado para {resource} ano={ano_efetivo}")
                return {
                    "fonte": "local",
                    "timestamp": None,
                    "ano": int(ano_efetivo),
                    "valor_total": "-",
                    "dados": dados
                }
            else:
                raise Exception(f"Formato de backup local inválido para {resource}")
    elif os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        filtrado = df[df.apply(lambda row: any(str(row[k]).strip() == str(ano) for k in row.index if k.lower() == "ano"), axis=1)]
        dados = filtrado.to_dict(orient="records")
        if not dados and ano != ano_default:
            filtrado_default = df[df.apply(lambda row: any(str(row[k]).strip() == str(ano_default) for k in row.index if k.lower() == "ano"), axis=1)]
            dados = filtrado_default.to_dict(orient="records")
            if dados:
                ano_efetivo = ano_default
        logging.info(f"Backup CSV carregado para {resource} ano={ano_efetivo}")
    else:
        raise Exception(f"Backup local não encontrado para {resource} ano={ano}")

    if not dados:
        raise Exception(f"Backup local não contém dados para {resource} ano={ano} nem para o ano default {ano_default}")

    # Extrair valor_total
    valor_total = ""
    if resource in ("importacao", "exportacao"):
        # Somar 'Valor (US$)' ignorando linhas sem o campo
        try:
            valores = [float(str(row.get("Valor (US$)", "0")).replace(".", "").replace(",", ".")) for row in dados if "Valor (US$)" in row and str(row["Valor (US$)"]).strip()]
            total = sum(valores)
            valor_total = f"{total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        except Exception as e:
            logging.warning(f"Erro ao somar valor total para {resource}: {e}")
            valor_total = ""
    else:
        # Somar 'Quantidade (L.)' ignorando linhas sem o campo
        try:
            quantidades = [float(str(row.get("Quantidade (L.)", "0")).replace(".", "").replace(",", ".")) for row in dados if "Quantidade (L.)" in row and str(row["Quantidade (L.)"]).strip()]
            total = sum(quantidades)
            valor_total = f"{total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        except Exception as e:
            logging.warning(f"Erro ao somar quantidade total para {resource}: {e}")
            valor_total = ""

    return {"dados": dados, "valor_total": valor_total, "ano": int(ano_efetivo)}

