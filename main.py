from filmes   import listar_filmes, criar_filme, atualizar_filme, deletar_filme
from clientes import listar_clientes, criar_cliente, atualizar_cliente, deletar_cliente
from alugueis import listar_alugueis, registrar_aluguel, registrar_devolucao
from vendas   import listar_vendas, registrar_venda

# Função genérica que exibe qualquer menu e executa a opção escolhida
def executar_menu(titulo, opcoes):
    while True:
        print(f"\n===== {titulo} =====")
        for chave, (descricao, _) in opcoes.items():
            print(f"  [{chave}] {descricao}")

        escolha = input("\nEscolha: ").strip()

        if escolha == "0":
            break
        elif escolha in opcoes:
            opcoes[escolha][1]()  # Chama a função da opção escolhida
        else:
            print("Opção inválida.")

def menu_filmes():
    executar_menu("FILMES", {
        "1": ("Listar filmes",   listar_filmes),
        "2": ("Cadastrar filme", criar_filme),
        "3": ("Atualizar filme", atualizar_filme),
        "4": ("Remover filme",   deletar_filme),
        "0": ("Voltar",          None),
    })

def menu_clientes():
    executar_menu("CLIENTES", {
        "1": ("Listar clientes",   listar_clientes),
        "2": ("Cadastrar cliente", criar_cliente),
        "3": ("Atualizar cliente", atualizar_cliente),
        "4": ("Remover cliente",   deletar_cliente),
        "0": ("Voltar",            None),
    })

def menu_alugueis():
    executar_menu("ALUGUÉIS", {
        "1": ("Listar aluguéis",     listar_alugueis),
        "2": ("Registrar aluguel",   registrar_aluguel),
        "3": ("Registrar devolução", registrar_devolucao),
        "0": ("Voltar",              None),
    })

def menu_vendas():
    executar_menu("VENDAS", {
        "1": ("Listar vendas",   listar_vendas),
        "2": ("Registrar venda", registrar_venda),
        "0": ("Voltar",          None),
    })

def main():
    # Dicionário que mapeia cada opção ao seu menu
    menus = {
        "1": menu_filmes,
        "2": menu_clientes,
        "3": menu_alugueis,
        "4": menu_vendas
    }

    while True:
        print("\n╔══════════════════════════╗")
        print("║     🎬 LOCADORA PYTHON   ║")
        print("╠══════════════════════════╣")
        print("║  [1] Filmes              ║")
        print("║  [2] Clientes            ║")
        print("║  [3] Aluguéis            ║")
        print("║  [4] Vendas              ║")
        print("║  [0] Sair                ║")
        print("╚══════════════════════════╝")

        escolha = input("\nEscolha: ").strip()

        if escolha == "0":
            print("\nAté logo! 👋")
            break
        elif escolha in menus:
            menus[escolha]()  # Chama o menu correspondente
        else:
            print("Opção inválida.")

# Ponto de entrada do programa
if __name__ == "__main__":
    main()
