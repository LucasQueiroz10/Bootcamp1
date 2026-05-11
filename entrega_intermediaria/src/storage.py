
import json
import os

CAMINHO_ARQUIVO = os.path.join(
    os.path.dirname(__file__),
    "..",
    "data",
    "gastos.json"
)


def carregar_dados(caminho=CAMINHO_ARQUIVO):

    if not os.path.exists(caminho):
        return {"gastos": [], "limite": None}

    with open(caminho, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def salvar_dados(dados, caminho=CAMINHO_ARQUIVO):

    diretorio = os.path.dirname(caminho)

    if diretorio and not os.path.exists(diretorio):
        os.makedirs(diretorio)

    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)
