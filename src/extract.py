import concurrent.futures
import logging
from concurrent.futures import as_completed

import requests
from pydantic import ValidationError
from tenacity import retry, stop_after_attempt, wait_exponential

from src.models import CryptoTicker

logger = logging.getLogger(__name__)


class CryptoAPIClient:
    def __init__(self):
        self.base_url = "https://www.mercadobitcoin.net/api"

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(3), reraise=True)
    def fetch_asset(self, ticker: str) -> dict:

        url_api = f"{self.base_url}/{ticker}/ticker/"

        response = requests.get(url=url_api, timeout=5)

        response.raise_for_status()

        dados_api = response.json()["ticker"]

        dados_api["ticker"] = ticker

        return dados_api

    def fetch_all_concurrently(self, tickers: list[str]) -> list[CryptoTicker]:

        objetos_validados = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futuros = {
                executor.submit(self.fetch_asset, ticker): ticker for ticker in tickers
            }

            for futuro in as_completed(futuros):
                ticker = futuros[futuro]
                try:
                    dado = futuro.result()
                    dado_validado = CryptoTicker(**dado)
                    objetos_validados.append(dado_validado)
                except requests.exceptions.RequestException as err_req:
                    logger.warning(f"Falha na rede ao buscar {ticker}: {err_req}")
                except ValidationError as err_val:
                    logger.error(f"Erro de validação no dado de {ticker}: {err_val}")

        return objetos_validados
