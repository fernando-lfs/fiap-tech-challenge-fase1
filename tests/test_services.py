"""
Testes unitários para o serviço de orquestração.
"""
import pytest
from app.services.vitibrasil_service import get_resource_data

@pytest.mark.parametrize("resource", [
    "producao", "processamento", "comercializacao", "importacao", "exportacao"
])
def test_get_resource_data(resource):
    resp = get_resource_data(resource)
    assert "fonte" in resp
    assert "timestamp" in resp
    assert "dados" in resp
    assert isinstance(resp["dados"], list)
