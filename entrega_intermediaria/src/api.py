
"""
api.py - Integração com APIs externas.
"""

import requests


def obter_cotacao_dolar():

    url = "https://economia.awesomeapi.com.br/json/last/USD-BRL"

    resposta = requests.get(url, timeout=5)

    if resposta.status_code != 200:
        raise Exception("Erro ao consultar API.")

    dados = resposta.json()

    cotacao = float(dados["USDBRL"]["bid"])

    return cotacao
