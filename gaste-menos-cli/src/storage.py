"""
storage.py - Responsável por salvar e carregar os dados do arquivo JSON.
"""

import json
import os

# Caminho padrão para o arquivo de dados
CAMINHO_ARQUIVO = os.path.join(os.path.dirname(__file__), "..", "data", "gastos.json")


def carregar_dados(caminho=CAMINHO_ARQUIVO):
    """
    Lê o arquivo JSON e retorna os dados salvos.
    Se o arquivo não existir, retorna uma estrutura padrão vazia.
    """
    if not os.path.exists(caminho):
        return {"gastos": [], "limite": None}

    with open(caminho, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def salvar_dados(dados, caminho=CAMINHO_ARQUIVO):
    """
    Salva os dados no arquivo JSON.
    Cria o diretório 'data' automaticamente se não existir.
    """
    diretorio = os.path.dirname(caminho)
    if diretorio and not os.path.exists(diretorio):
        os.makedirs(diretorio)

    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)
