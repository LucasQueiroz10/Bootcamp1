import requests

def obter_cotacao_dolar():
    url = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
    resposta = requests.get(url, timeout=5)
    resposta.raise_for_status()
    return float(resposta.json()["USDBRL"]["bid"])
