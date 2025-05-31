"""
Testes unitários para o serviço de orquestração.
"""
import pytest
from unittest.mock import patch
from app.services.scraping import get_resource_data

@pytest.mark.parametrize("resource", [
    "producao", "processamento", "comercializacao", "importacao", "exportacao"
])
def test_get_resource_data(resource):
    """Testa se o serviço retorna estrutura esperada para cada recurso (integração real)."""
    resp = get_resource_data(resource)
    assert "fonte" in resp
    assert "timestamp" in resp
    assert "dados" in resp
    assert isinstance(resp["dados"], list)


def test_fallback_to_local_backup_real_file():
    """Testa o fallback local REAL: simula falha no scraping e garante leitura do arquivo /data/producao.json.

    O método scrape_table lança exceção (site offline), e load_backup lê o arquivo real.
    """
    with patch("app.services.scraping.scrape_table", side_effect=Exception("Site offline")):
        resp = get_resource_data("producao", ano="2023")
        assert resp["fonte"] == "local"
        assert isinstance(resp["dados"], list)
        # Confere se os dados retornados batem com o conteúdo do producao.json filtrado por ano
        produtos = [row.get("produto") or row.get("Produto") for row in resp["dados"]]
        assert any(p and "Tinto" in p for p in produtos)
        assert any(p and "Branco" in p for p in produtos)
        assert resp["ano"] == 2023
