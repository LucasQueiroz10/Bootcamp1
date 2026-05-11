
from unittest.mock import patch
from src.api import obter_cotacao_dolar


@patch("src.api.requests.get")
def test_obter_cotacao_dolar(mock_get):

    mock_get.return_value.status_code = 200

    mock_get.return_value.json.return_value = {
        "USDBRL": {
            "bid": "5.50"
        }
    }

    cotacao = obter_cotacao_dolar()

    assert cotacao == 5.50
