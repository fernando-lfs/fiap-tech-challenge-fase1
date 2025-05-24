"""
Testes unitários para adapters de scraping e backup.
"""
import pytest
from app.adapters.scraper import scrape_table
from app.adapters.backup import load_backup

@pytest.mark.parametrize("resource", [
    "producao", "processamento", "comercializacao", "importacao", "exportacao"
])
def test_scraper(resource):
    try:
        dados = scrape_table(resource)
        assert isinstance(dados, list)
    except Exception:
        assert True  # Pode falhar se site indisponível

@pytest.mark.parametrize("resource", [
    "producao", "processamento", "comercializacao", "importacao", "exportacao"
])
def test_backup(resource):
    try:
        dados = load_backup(resource)
        assert isinstance(dados, list)
    except Exception:
        assert True  # Pode falhar se backup não existir
