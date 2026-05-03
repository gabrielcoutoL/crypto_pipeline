import pytest
from pydantic import ValidationError

from src.models import CryptoTicker
from src.transform import CryptoProcessor


def test_field_last():

    with pytest.raises(ValidationError):
        objeto_teste = CryptoTicker(ticker="TESTE", last="abc", high=1, low=1, vol=100)


def test_volume_rule():

    objetos_mockados = [
        CryptoTicker(ticker="TESTE1", last=100, high=1, low=1, vol=100),
        CryptoTicker(ticker="TESTE2", last=200, high=2, low=2, vol=100),
        CryptoTicker(ticker="TESTE3", last=300, high=3, low=3, vol=30),
    ]

    processador = CryptoProcessor(objetos_mockados)

    df_mock = processador.process()

    assert len(df_mock) == 2
