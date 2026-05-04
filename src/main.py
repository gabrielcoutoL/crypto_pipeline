import logging
from datetime import datetime
from pathlib import Path

from sqlalchemy import text

from src.database import DATABASE_URL, engine
from src.extract import CryptoAPIClient
from src.transform import CryptoProcessor

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def criar_tabela_execs(engine_db):

    with engine_db.begin() as conn:
        conn.execute(
            text(
                "CREATE TABLE IF NOT EXISTS execucoes_etl (id SERIAL PRIMARY KEY, data_execucao TIMESTAMP, status VARCHAR(50))"
            )
        )

        query_insert = text(
            "INSERT INTO execucoes_etl (data_execucao, status) VALUES (:data_now, :status)"
        )

        conn.execute(query_insert, {"data_now": datetime.now(), "status": "SUCESSO"})


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

    logging.info("Conectando no banco e registrando a execução.")
    criar_tabela_execs(engine)

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

        dados_transformados.write_database(
            table_name="tb_crypto_metrics",
            connection=DATABASE_URL,
            if_table_exists="replace",
        )
        logger.info("Dados salvos no banco de dados.")
    else:
        logger.warning("Nenhum dado válido foi retornado pela API. Pipeline abortado.")


if __name__ == "__main__":
    main()
