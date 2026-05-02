import polars as pl

from src.models import CryptoTicker


class CryptoProcessor:
    def __init__(self, data: list[CryptoTicker]):

        self.df_crypto = pl.DataFrame(data)

    def process(self) -> pl.DataFrame:
        df_transformado = (
            self.df_crypto.with_columns(spread_reais=pl.col("high") - pl.col("low"))
            .filter(pl.col("vol") > 50.0)
            .sort(pl.col("spread_reais"), descending=True)
        )

        return df_transformado
