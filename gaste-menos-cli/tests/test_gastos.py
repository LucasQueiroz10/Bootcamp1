"""
tests/test_gastos.py - Testes automatizados para a lógica de negócio.
Execute com: pytest tests/
"""

import os
import sys

# Permite importar os módulos da pasta src durante os testes
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from gastos import (
    adicionar_gasto,
    calcular_total,
    definir_limite,
    listar_gastos,
    remover_gasto,
    verificar_limite,
)

# ──────────────────────────────────────────────
# Fixtures auxiliares
# ──────────────────────────────────────────────

def dados_vazios():
    """Retorna uma estrutura de dados limpa para cada teste."""
    return {"gastos": [], "limite": None}


# ──────────────────────────────────────────────
# Testes de SUCESSO
# ──────────────────────────────────────────────

def test_adicionar_gasto_valido():
    """Deve adicionar um gasto com descrição e valor válidos."""
    dados = dados_vazios()
    sucesso, mensagem = adicionar_gasto(dados, "Almoço", 25.50)

    assert sucesso is True
    assert len(dados["gastos"]) == 1
    assert dados["gastos"][0]["descricao"] == "Almoço"
    assert dados["gastos"][0]["valor"] == 25.50


def test_adicionar_multiplos_gastos():
    """Deve adicionar múltiplos gastos com IDs incrementais."""
    dados = dados_vazios()
    adicionar_gasto(dados, "Café", 5.00)
    adicionar_gasto(dados, "Ônibus", 4.50)
    adicionar_gasto(dados, "Lanche", 12.00)

    assert len(dados["gastos"]) == 3
    assert dados["gastos"][0]["id"] == 1
    assert dados["gastos"][1]["id"] == 2
    assert dados["gastos"][2]["id"] == 3


def test_remover_gasto_existente():
    """Deve remover um gasto pelo ID corretamente."""
    dados = dados_vazios()
    adicionar_gasto(dados, "Cinema", 30.00)
    id_gasto = dados["gastos"][0]["id"]

    sucesso, mensagem = remover_gasto(dados, id_gasto)

    assert sucesso is True
    assert len(dados["gastos"]) == 0


def test_calcular_total_com_gastos():
    """Deve somar corretamente todos os valores dos gastos."""
    dados = dados_vazios()
    adicionar_gasto(dados, "Mercado", 100.00)
    adicionar_gasto(dados, "Farmácia", 50.00)

    total = calcular_total(dados)

    assert total == 150.00


def test_definir_limite_valido():
    """Deve definir o limite quando o valor for positivo."""
    dados = dados_vazios()
    sucesso, mensagem = definir_limite(dados, 500.00)

    assert sucesso is True
    assert dados["limite"] == 500.00


def test_limite_nao_ultrapassado():
    """Deve retornar False quando o total está abaixo do limite."""
    dados = dados_vazios()
    adicionar_gasto(dados, "Jantar", 40.00)
    definir_limite(dados, 200.00)

    ultrapassou = verificar_limite(dados)

    assert ultrapassou is False


def test_limite_ultrapassado():
    """Deve retornar True quando o total ultrapassa o limite."""
    dados = dados_vazios()
    adicionar_gasto(dados, "Notebook", 3000.00)
    definir_limite(dados, 1000.00)

    ultrapassou = verificar_limite(dados)

    assert ultrapassou is True


# ──────────────────────────────────────────────
# Testes de ERRO (entradas inválidas)
# ──────────────────────────────────────────────

def test_adicionar_gasto_valor_negativo():
    """Deve rejeitar um gasto com valor negativo."""
    dados = dados_vazios()
    sucesso, mensagem = adicionar_gasto(dados, "Erro", -10.00)

    assert sucesso is False
    assert len(dados["gastos"]) == 0


def test_adicionar_gasto_valor_zero():
    """Deve rejeitar um gasto com valor igual a zero."""
    dados = dados_vazios()
    sucesso, mensagem = adicionar_gasto(dados, "Grátis", 0)

    assert sucesso is False


def test_adicionar_gasto_valor_texto():
    """Deve rejeitar um gasto quando o valor não é numérico."""
    dados = dados_vazios()
    sucesso, mensagem = adicionar_gasto(dados, "Teste", "abc")

    assert sucesso is False
    assert len(dados["gastos"]) == 0


def test_adicionar_gasto_descricao_vazia():
    """Deve rejeitar um gasto com descrição vazia."""
    dados = dados_vazios()
    sucesso, mensagem = adicionar_gasto(dados, "   ", 20.00)

    assert sucesso is False
    assert len(dados["gastos"]) == 0


def test_remover_gasto_id_inexistente():
    """Deve retornar erro ao tentar remover um ID que não existe."""
    dados = dados_vazios()
    sucesso, mensagem = remover_gasto(dados, 999)

    assert sucesso is False


def test_remover_gasto_id_invalido():
    """Deve retornar erro ao informar ID não numérico."""
    dados = dados_vazios()
    sucesso, mensagem = remover_gasto(dados, "xyz")

    assert sucesso is False


def test_definir_limite_negativo():
    """Deve rejeitar um limite com valor negativo."""
    dados = dados_vazios()
    sucesso, mensagem = definir_limite(dados, -100)

    assert sucesso is False
    assert dados["limite"] is None


def test_definir_limite_texto():
    """Deve rejeitar um limite não numérico."""
    dados = dados_vazios()
    sucesso, mensagem = definir_limite(dados, "muito")

    assert sucesso is False


# ──────────────────────────────────────────────
# Testes de CASO LIMITE (edge cases)
# ──────────────────────────────────────────────

def test_total_lista_vazia():
    """Deve retornar 0.0 quando não há gastos cadastrados."""
    dados = dados_vazios()
    total = calcular_total(dados)

    assert total == 0.0


def test_listar_gastos_lista_vazia():
    """Deve retornar uma lista vazia quando não há gastos."""
    dados = dados_vazios()
    gastos = listar_gastos(dados)

    assert gastos == []


def test_verificar_limite_sem_limite_definido():
    """Deve retornar None quando nenhum limite foi definido."""
    dados = dados_vazios()
    adicionar_gasto(dados, "Algo", 50.00)

    resultado = verificar_limite(dados)

    assert resultado is None


def test_limite_exatamente_igual_ao_total():
    """Deve retornar False quando total é igual ao limite (não ultrapassou)."""
    dados = dados_vazios()
    adicionar_gasto(dados, "Gasto exato", 100.00)
    definir_limite(dados, 100.00)

    ultrapassou = verificar_limite(dados)

    assert ultrapassou is False


def test_adicionar_gasto_id_continua_apos_remocao():
    """IDs não devem ser reutilizados após remoção."""
    dados = dados_vazios()
    adicionar_gasto(dados, "Item A", 10.00)
    adicionar_gasto(dados, "Item B", 20.00)
    remover_gasto(dados, 1)
    adicionar_gasto(dados, "Item C", 30.00)

    ids = [g["id"] for g in dados["gastos"]]
    # O novo gasto deve ter ID 3, não reutilizar o ID 1
    assert 1 not in ids
    assert 3 in ids
