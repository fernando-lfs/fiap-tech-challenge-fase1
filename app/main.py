"""
Módulo principal da API Vitibrasil.
Instancia o FastAPI, inclui routers, configura logs e CORS.
"""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings, setup_logging
from app.routers.vitibrasil_router import router as vitibrasil_router

setup_logging()

app = FastAPI(title="Vitibrasil API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(vitibrasil_router)

@app.get("/health", tags=["health"])
def health_check():
    """Endpoint para checagem de saúde da API."""
    return {"status": "ok"}
