"""
Módulo principal da API Vitibrasil.
Instancia o FastAPI, inclui routers, configura logs e CORS.
"""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings, setup_logging
from app.routes import router_dados, router_auth, router_utils
from app.services import check_site_status

setup_logging()

app = FastAPI(title="Vitibrasil API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_dados)
app.include_router(router_auth)
app.include_router(router_utils)

@app.get("/health", tags=["Utilitários"], summary="Teste de saúde da API")
def health_check():
    """Retorna status do servidor FastAPI e status do site da Embrapa."""
    return {
        "api": "online",
        "site_embrapa_online": check_site_status()
    }
