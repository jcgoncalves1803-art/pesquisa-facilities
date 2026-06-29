import requests
from functools import lru_cache
from config import IBGE_API_BASE


class IBGEService:

    @staticmethod
    @lru_cache(maxsize=1)
    def listar_estados():
        url = f"{IBGE_API_BASE}/localidades/estados"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            estados = response.json()
            return sorted(estados, key=lambda x: x["nome"])
        except requests.RequestException as e:
            print(f"Erro API IBGE: {e}")
            return []

    @staticmethod
    @lru_cache(maxsize=27)
    def listar_municipios(uf_id):
        url = f"{IBGE_API_BASE}/localidades/estados/{uf_id}/municipios"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            municipios = response.json()
            return sorted(municipios, key=lambda x: x["nome"])
        except requests.RequestException as e:
            print(f"Erro API IBGE: {e}")
            return []
