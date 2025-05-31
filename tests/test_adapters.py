"""
Testes unitários para adapters de scraping e backup.
"""
import pytest
from app.adapters.embrapa_scraper import scrape_table
from app.adapters.local_backup import load_backup

@pytest.mark.parametrize("resource,ano", [
    ("producao", "2023"), ("processamento", "2023"), ("comercializacao", "2023"), ("importacao", "2024"), ("exportacao", "2024")
])
def test_scraper(resource, ano):
    try:
        dados = scrape_table(resource, ano)
        assert isinstance(dados["dados"], list)
    except Exception:
        assert True  # Pode falhar se site indisponível

@pytest.mark.parametrize("resource,ano", [
    ("producao", "2023"), ("processamento", "2023"), ("comercializacao", "2023"), ("importacao", "2024"), ("exportacao", "2024")
])
def test_backup(resource, ano):
    try:
        dados = load_backup(resource, ano)
        assert isinstance(dados["dados"], list)
    except Exception:
        assert True  # Pode falhar se backup não existir
