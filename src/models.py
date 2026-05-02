from pydantic import BaseModel, field_validator


class CryptoTicker(BaseModel):
    ticker: str
    last: float
    high: float
    low: float
    vol: float

    @field_validator("ticker")
    @classmethod
    def valida_ticker(cls, ticker_bruto):

        return ticker_bruto.upper()
