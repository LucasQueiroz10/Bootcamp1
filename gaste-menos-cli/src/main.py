"""
main.py - Interface de linha de comando (CLI) do Gaste Menos.
Execute com: python src/main.py
"""

import os
import sys

# Garante que o Python encontre os módulos da pasta src
sys.path.insert(0, os.path.dirname(__file__))

from gastos import (
    adicionar_gasto,
    calcular_total,
    definir_limite,
    listar_gastos,
    remover_gasto,
    verificar_limite,
)
from storage import carregar_dados, salvar_dados

# ──────────────────────────────────────────────
# Funções de exibição
# ──────────────────────────────────────────────

def exibir_cabecalho():
    print("\n" + "=" * 45)
    print("       💸  GASTE MENOS CLI  v1.0.0")
    print("=" * 45)


def exibir_menu():
    print("\n📋  O QUE DESEJA FAZER?")
    print("  [1] Adicionar gasto")
    print("  [2] Listar gastos")
    print("  [3] Ver total gasto")
    print("  [4] Definir limite de gastos")
    print("  [5] Remover um gasto")
    print("  [0] Sair")
    print("-" * 45)


def exibir_gastos(dados):
    gastos = listar_gastos(dados)

    if not gastos:
        print("\n⚠️  Nenhum gasto cadastrado ainda.")
        return

    print("\n📂  SEUS GASTOS:")
    print(f"  {'ID':<5} {'Descrição':<25} {'Valor':>10}")
    print("  " + "-" * 42)

    for gasto in gastos:
        print(f"  {gasto['id']:<5} {gasto['descricao']:<25} R$ {gasto['valor']:>7.2f}")

    total = calcular_total(dados)
    print("  " + "-" * 42)
    print(f"  {'TOTAL':<30} R$ {total:>7.2f}")

    # Exibe informação sobre o limite
    if dados["limite"] is not None:
        print(f"  {'LIMITE':<30} R$ {dados['limite']:>7.2f}")
        ultrapassou = verificar_limite(dados)
        if ultrapassou:
            print("\n  🚨  ATENÇÃO: Você ultrapassou o seu limite de gastos!")
        else:
            restante = dados["limite"] - total
            print(f"\n  ✅  Você ainda pode gastar R$ {restante:.2f}.")


def exibir_alerta_limite(dados):
    """
    Exibe um alerta imediato se o limite for ultrapassado
    após adicionar um gasto.
    """
    ultrapassou = verificar_limite(dados)
    if ultrapassou is True:
        print("\n  🚨  ALERTA: Limite de gastos ultrapassado!")


# ──────────────────────────────────────────────
# Fluxos de cada opção do menu
# ──────────────────────────────────────────────

def fluxo_adicionar(dados):
    print("\n➕  ADICIONAR GASTO")
    descricao = input("  Descrição: ")
    valor_str = input("  Valor (R$): ")

    sucesso, mensagem = adicionar_gasto(dados, descricao, valor_str)
    print(f"\n  {'✅' if sucesso else '❌'}  {mensagem}")

    if sucesso:
        salvar_dados(dados)
        exibir_alerta_limite(dados)


def fluxo_remover(dados):
    exibir_gastos(dados)

    if not listar_gastos(dados):
        return

    print("\n🗑️  REMOVER GASTO")
    id_str = input("  Informe o ID do gasto a remover: ")

    sucesso, mensagem = remover_gasto(dados, id_str)
    print(f"\n  {'✅' if sucesso else '❌'}  {mensagem}")

    if sucesso:
        salvar_dados(dados)


def fluxo_definir_limite(dados):
    print("\n🎯  DEFINIR LIMITE DE GASTOS")
    if dados["limite"] is not None:
        print(f"  Limite atual: R$ {dados['limite']:.2f}")
    limite_str = input("  Novo limite (R$): ")

    sucesso, mensagem = definir_limite(dados, limite_str)
    print(f"\n  {'✅' if sucesso else '❌'}  {mensagem}")

    if sucesso:
        salvar_dados(dados)


def fluxo_total(dados):
    total = calcular_total(dados)
    print(f"\n💰  TOTAL GASTO: R$ {total:.2f}")

    if dados["limite"] is not None:
        print(f"    LIMITE DEFINIDO: R$ {dados['limite']:.2f}")
        ultrapassou = verificar_limite(dados)
        if ultrapassou:
            print("    🚨  Limite ULTRAPASSADO!")
        else:
            restante = dados["limite"] - total
            print(f"    ✅  Restante: R$ {restante:.2f}")
    else:
        print("    ℹ️  Nenhum limite definido. Use a opção [4] para definir.")


# ──────────────────────────────────────────────
# Loop principal
# ──────────────────────────────────────────────

def main():
    exibir_cabecalho()
    dados = carregar_dados()

    while True:
        exibir_menu()
        opcao = input("  Escolha uma opção: ").strip()

        if opcao == "1":
            fluxo_adicionar(dados)

        elif opcao == "2":
            exibir_gastos(dados)

        elif opcao == "3":
            fluxo_total(dados)

        elif opcao == "4":
            fluxo_definir_limite(dados)

        elif opcao == "5":
            fluxo_remover(dados)

        elif opcao == "0":
            print("\n👋  Até logo! Continue controlando seus gastos.\n")
            break

        else:
            print("\n  ❌  Opção inválida. Escolha um número entre 0 e 5.")


if __name__ == "__main__":
    main()
