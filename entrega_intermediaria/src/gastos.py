"""
gastos.py - Contém toda a lógica de negócio relacionada aos gastos.
"""


def adicionar_gasto(dados, descricao, valor):
    """
    Adiciona um novo gasto à lista.

    Regras:
    - A descrição não pode ser vazia.
    - O valor não pode ser negativo ou zero.

    Retorna (True, mensagem) em caso de sucesso,
    ou (False, mensagem) em caso de erro.
    """
    descricao = descricao.strip()

    if not descricao:
        return False, "A descrição não pode ser vazia."

    try:
        valor = float(valor)
    except (ValueError, TypeError):
        return False, "O valor informado não é um número válido."

    if valor <= 0:
        return False, "O valor deve ser maior que zero."

    # Cria o gasto como um dicionário simples
    gasto = {
        "id": _proximo_id(dados["gastos"]),
        "descricao": descricao,
        "valor": valor,
    }

    dados["gastos"].append(gasto)
    return True, f"Gasto '{descricao}' de R$ {valor:.2f} adicionado com sucesso!"


def remover_gasto(dados, id_gasto):
    """
    Remove um gasto da lista pelo seu ID.

    Retorna (True, mensagem) em caso de sucesso,
    ou (False, mensagem) se o ID não for encontrado.
    """
    try:
        id_gasto = int(id_gasto)
    except (ValueError, TypeError):
        return False, "ID inválido. Informe um número inteiro."

    for i, gasto in enumerate(dados["gastos"]):
        if gasto["id"] == id_gasto:
            removido = dados["gastos"].pop(i)
            return True, f"Gasto '{removido['descricao']}' removido com sucesso!"

    return False, f"Gasto com ID {id_gasto} não encontrado."


def calcular_total(dados):
    """
    Soma todos os valores dos gastos cadastrados.
    Retorna 0.0 se não houver gastos.
    """
    return sum(gasto["valor"] for gasto in dados["gastos"])


def definir_limite(dados, limite):
    """
    Define o limite máximo de gastos.

    Retorna (True, mensagem) em caso de sucesso,
    ou (False, mensagem) se o valor for inválido.
    """
    try:
        limite = float(limite)
    except (ValueError, TypeError):
        return False, "O limite informado não é um número válido."

    if limite <= 0:
        return False, "O limite deve ser maior que zero."

    dados["limite"] = limite
    return True, f"Limite definido para R$ {limite:.2f}."


def verificar_limite(dados):
    """
    Verifica se o total de gastos ultrapassou o limite definido.

    Retorna:
    - None se nenhum limite foi definido.
    - True se o limite foi ultrapassado.
    - False se ainda está dentro do limite.
    """
    if dados["limite"] is None:
        return None

    total = calcular_total(dados)
    return total > dados["limite"]


def listar_gastos(dados):
    """
    Retorna a lista de gastos cadastrados.
    Pode ser uma lista vazia se não houver gastos.
    """
    return dados["gastos"]


# ──────────────────────────────────────────────
# Funções auxiliares (uso interno)
# ──────────────────────────────────────────────

def _proximo_id(gastos):
    """
    Gera um ID único e incremental para o próximo gasto.
    """
    if not gastos:
        return 1
    return max(g["id"] for g in gastos) + 1
