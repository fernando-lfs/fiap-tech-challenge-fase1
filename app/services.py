"""
Serviços para scraping, fallback, manipulação de usuários e utilitários.
"""
import os
import json
from typing import Dict, List, Optional
from datetime import datetime
from app.adapters import scrape_table, load_backup
from app.core.config import settings
import logging

USERS_FILE = os.path.join(settings.backup_path, "users.json")

DEFAULT_USER = {"username": "admin", "password": "admin123"}

def ensure_users_file():
    """Garante que o arquivo de usuários existe e contém o usuário default."""
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump([DEFAULT_USER], f)
    else:
        with open(USERS_FILE, "r+", encoding="utf-8") as f:
            try:
                users = json.load(f)
            except Exception:
                users = []
            if not any(u["username"] == DEFAULT_USER["username"] for u in users):
                users.append(DEFAULT_USER)
                f.seek(0)
                json.dump(users, f)
                f.truncate()

def get_all_users() -> List[Dict]:
    ensure_users_file()
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def add_user(username: str, password: str) -> None:
    users = get_all_users()
    if any(u["username"] == username for u in users):
        raise ValueError("Usuário já existe.")
    users.append({"username": username, "password": password})
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f)

def authenticate_user(username: str, password: str) -> bool:
    users = get_all_users()
    return any(u["username"] == username and u["password"] == password for u in users)

def get_resource_data(resource: str, ano: Optional[str] = None) -> Dict:
    """
    Orquestra obtenção de dados: tenta scraping, faz fallback para backup local, filtra por ano.
    Args:
        resource (str): Nome do recurso.
        ano (str, opcional): Ano para filtro. Default: '2024'.
    Returns:
        Dict: Dicionário com fonte, timestamp e dados.
    """
    ano = ano or "2024"
    try:
        dados = scrape_table(resource, ano)
        fonte = "online"
    except Exception:
        dados = load_backup(resource, ano)
        fonte = "local"
    resp = {
        "fonte": fonte,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "dados": dados
    }
    logging.info(f"Fonte dos dados de {resource}: {fonte}")
    return resp

def check_site_status() -> bool:
    """Verifica se o site da Embrapa está online."""
    import requests
    try:
        resp = requests.get("http://vitibrasil.cnpuv.embrapa.br", timeout=10)
        return resp.status_code == 200
    except Exception:
        return False
