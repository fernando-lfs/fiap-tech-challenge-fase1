import requests

def check_site_status() -> bool:
    """Verifica se o site da Embrapa está online."""
    try:
        resp = requests.get("http://vitibrasil.cnpuv.embrapa.br", timeout=10)
        return resp.status_code == 200
    except Exception:
        return False

