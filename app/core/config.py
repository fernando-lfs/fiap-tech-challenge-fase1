"""
Configuração central da aplicação.
Carrega variáveis de ambiente e define settings globais.
"""
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
import logging

load_dotenv()

class Settings(BaseSettings):
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "supersecretkey")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    jwt_expire_minutes: int = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", 60))
    backup_path: str = os.getenv("BACKUP_PATH", "./data")
    log_path: str = os.getenv("LOG_PATH", "./logs/app.log")

settings = Settings()

def setup_logging():
    """Configura logging para arquivo e console."""
    os.makedirs(os.path.dirname(settings.log_path), exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s [%(name)s] %(message)s',
        handlers=[
            logging.FileHandler(settings.log_path),
            logging.StreamHandler()
        ]
    )
