"""
Leitura de backups locais (CSV/JSON) para fallback.
"""
import os
import json
import pandas as pd
from typing import List, Any
from app.core.config import settings
import logging

def load_backup(resource: str) -> List[Any]:
    """
    Carrega backup local (CSV ou JSON) do recurso.
    Args:
        resource (str): Nome do recurso.
    Returns:
        List[Any]: Dados do backup.
    Raises:
        Exception: Se não encontrar backup válido.
    """
    backup_dir = settings.backup_path
    csv_path = os.path.join(backup_dir, f"{resource}.csv")
    json_path = os.path.join(backup_dir, f"{resource}.json")
    logging.info(f"Tentando carregar backup local para {resource}")
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            logging.info(f"Backup JSON carregado para {resource}")
            return data
    elif os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        data = df.to_dict(orient="records")
        logging.info(f"Backup CSV carregado para {resource}")
        return data
    else:
        logging.error(f"Backup local não encontrado para {resource}")
        raise FileNotFoundError(f"Backup local não encontrado para {resource}")
