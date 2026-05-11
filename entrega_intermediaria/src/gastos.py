
"""
gastos.py - Contém toda a lógica de negócio relacionada aos gastos.
"""

def adicionar_gasto(dados, descricao, valor):

    descricao = descricao.strip()

    if not descricao:
        return False, "A descrição não pode ser vazia."

    try:
        valor = float(valor)

    except (ValueError, TypeError):
        return False, "O valor informado não é válido."

    if valor <= 0:
        return False, "O valor deve ser maior que zero."

    gasto = {
        "id": _proximo_id(dados["gastos"]),
        "descricao": descricao,
        "valor": valor,
    }

    dados["gastos"].append(gasto)

    return True, f"Gasto '{descricao}' adicionado com sucesso!"


def remover_gasto(dados, id_gasto):

    try:
        id_gasto = int(id_gasto)

    except (ValueError, TypeError):
        return False, "ID inválido."

    for i, gasto in enumerate(dados["gastos"]):

        if gasto["id"] == id_gasto:
            removido = dados["gastos"].pop(i)

            return True, f"Gasto '{removido['descricao']}' removido."

    return False, "Gasto não encontrado."


def calcular_total(dados):

    return sum(gasto["valor"] for gasto in dados["gastos"])


def definir_limite(dados, limite):

    try:
        limite = float(limite)

    except (ValueError, TypeError):
        return False, "Limite inválido."

    if limite <= 0:
        return False, "O limite deve ser maior que zero."

    dados["limite"] = limite

    return True, f"Limite definido para R$ {limite:.2f}."


def verificar_limite(dados):

    if dados["limite"] is None:
        return None

    total = calcular_total(dados)

    return total > dados["limite"]


def listar_gastos(dados):

    return dados["gastos"]


def _proximo_id(gastos):

    if not gastos:
        return 1

    return max(g["id"] for g in gastos) + 1
