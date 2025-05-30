import os
import json
from typing import Dict, List
from app.core.config import settings

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

