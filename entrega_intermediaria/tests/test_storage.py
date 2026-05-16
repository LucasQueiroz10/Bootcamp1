"""
tests/test_storage.py - Testes para a camada de persistência de dados.
"""

import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from storage import carregar_dados, salvar_dados


def test_carregar_dados_arquivo_inexistente():
    """Deve retornar estrutura padrão quando o arquivo não existe."""
    caminho_falso = "/tmp/arquivo_que_nao_existe_12345.json"
    dados = carregar_dados(caminho_falso)

    assert dados == {"gastos": [], "limite": None}


def test_salvar_e_carregar_dados():
    """Deve salvar e recarregar os dados corretamente."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False
    ) as arquivo_temp:
        caminho = arquivo_temp.name

    try:
        dados_originais = {
            "gastos": [{"id": 1, "descricao": "Teste", "valor": 42.0}],
            "limite": 200.0,
        }

        salvar_dados(dados_originais, caminho)
        dados_carregados = carregar_dados(caminho)

        assert dados_carregados["gastos"][0]["descricao"] == "Teste"
        assert dados_carregados["limite"] == 200.0

    finally:
        os.unlink(caminho)


def test_salvar_cria_diretorio_automaticamente():
    """Deve criar o diretório de destino se ele não existir."""
    with tempfile.TemporaryDirectory() as pasta_temp:
        caminho = os.path.join(pasta_temp, "subpasta", "gastos.json")
        dados = {"gastos": [], "limite": None}

        salvar_dados(dados, caminho)

        assert os.path.exists(caminho)
