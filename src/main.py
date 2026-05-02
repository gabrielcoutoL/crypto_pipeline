import logging
from pathlib import Path

from src.extract import CryptoAPIClient
from src.transform import CryptoProcessor

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


# Lista de criptos com 2 moedas falsas pra simular erro
def main():
    coins = [
        "BTC",
        "ETH",
        "SOL",
        "DOGE",
        "USDC",
        "ASSET_FALSO_1",
        "LINK",
        "ASSET_FALSO_2",
    ]

    logger = logging.getLogger(__name__)
    logger.info("Iniciando pipeline de extração de criptoativos...")

    # Extração
    extrator = CryptoAPIClient()
    lista_objetos = extrator.fetch_all_concurrently(coins)

    # Processamento dos dados e transformação
    if lista_objetos:
        logger.info(f"Processando {len(lista_objetos)} ativos validados...")
        processador = CryptoProcessor(lista_objetos)
        dados_transformados = processador.process()

        # caminhos
        caminho_base = Path.cwd()
        destino = caminho_base / "data" / "bronze" / "arquivo_final.parquet"

        # Cria o caminho /data/bronze
        destino.parent.mkdir(parents=True, exist_ok=True)

        # Salva o arquivo em parquet
        dados_transformados.write_parquet(destino)
        logger.info(f"Pipeline finalizado com sucesso! Arquivo salvo em: {destino}")
    else:
        logger.warning("Nenhum dado válido foi retornado pela API. Pipeline abortado.")


if __name__ == "__main__":
    main()
