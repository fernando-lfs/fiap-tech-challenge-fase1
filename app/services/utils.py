import requests

def check_site_status() -> bool:
    """
    Verificar se o site da Embrapa está online.

    Returns:
        bool: True se o site estiver online, False caso contrário.
    """
    """Verifica se o site da Embrapa está online."""
    try:
        resp = requests.get("http://vitibrasil.cnpuv.embrapa.br", timeout=10)
        return resp.status_code == 200
    except Exception:
        return False

