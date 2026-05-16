from unittest.mock import patch
from src.api import obter_cotacao_dolar

@patch("src.api.requests.get")
def test_obter_cotacao_dolar(mock_get):
    mock_get.return_value.raise_for_status.return_value = None
    mock_get.return_value.json.return_value = {"USDBRL":{"bid":"5.50"}}
    assert obter_cotacao_dolar() == 5.50
