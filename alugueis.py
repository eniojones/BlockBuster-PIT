from database import carregar, salvar, buscar_por_id, novo_id
from filmes import listar_filmes
from clientes import listar_clientes
from datetime import date

def registrar_aluguel():
    print("\n--- Filmes disponíveis ---")
    listar_filmes()
    print("\n--- Clientes cadastrados ---")
    listar_clientes()

    dados = carregar()

    try:
        id_filme   = int(input("\nID do filme a alugar: "))
        id_cliente = int(input("ID do cliente: "))
        dias       = int(input("Quantidade de dias: "))
        valor      = float(input("Valor do aluguel (R$): "))
    except ValueError:
        print("Entrada inválida.")
        return

    filme   = buscar_por_id(dados["filmes"], id_filme)
    cliente = buscar_por_id(dados["clientes"], id_cliente)

    if not filme:
        print("Filme não encontrado."); return
    if not filme["disponivel"]:
        print("Filme indisponível."); return
    if not cliente:
        print("Cliente não encontrado."); return

    aluguel = {
        "id": novo_id(dados["alugueis"]),
        "id_filme": id_filme,
        "titulo_filme": filme["titulo"],
        "id_cliente": id_cliente,
        "nome_cliente": cliente["nome"],
        "data": str(date.today()),
        "dias": dias,
        "valor": valor,
        "devolvido": False
    }
    dados["alugueis"].append(aluguel)

    filme["disponivel"] = False

    salvar(dados)
    print(f'\nAluguel #{aluguel["id"]} registrado! "{filme["titulo"]}" para {cliente["nome"]}.')

def listar_alugueis():
    dados    = carregar()
    alugueis = dados["alugueis"]

    if not alugueis:
        print("\nNenhum aluguel registrado.")
        return

    print(f'\n{"ID":<5} {"Filme":<25} {"Cliente":<20} {"Data":<12} {"Dias":<6} {"Valor":<10} {"Devolvido"}')
    print("-" * 85)

    for a in alugueis:
        devolvido = "Sim" if a["devolvido"] else "Não"
        print(f'{a["id"]:<5} {a["titulo_filme"]:<25} {a["nome_cliente"]:<20} '
              f'{a["data"]:<12} {a["dias"]:<6} R${a["valor"]:<9.2f} {devolvido}')

def registrar_devolucao():
    listar_alugueis()

    try:
        id_alvo = int(input("\nID do aluguel a devolver: "))
    except ValueError:
        print("ID inválido."); return

    dados   = carregar()
    aluguel = buscar_por_id(dados["alugueis"], id_alvo)

    if not aluguel:
        print("Aluguel não encontrado."); return
    if aluguel["devolvido"]:
        print("Este filme já foi devolvido."); return

    aluguel["devolvido"] = True

    filme = buscar_por_id(dados["filmes"], aluguel["id_filme"])
    if filme:
        filme["disponivel"] = True

    salvar(dados)
    print(f"Devolução do aluguel #{id_alvo} registrada!")
