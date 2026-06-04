from database import carregar, salvar, buscar_por_id, novo_id
from filmes import listar_filmes
from clientes import listar_clientes
from datetime import date

def registrar_venda():
    print("\n--- Filmes disponíveis ---")
    listar_filmes()
    print("\n--- Clientes cadastrados ---")
    listar_clientes()

    dados = carregar()

    try:
        id_filme   = int(input("\nID do filme a vender: "))
        id_cliente = int(input("ID do cliente: "))
        valor      = float(input("Valor da venda (R$): "))
    except ValueError:
        print("❌ Entrada inválida."); return

    # Busca o filme e o cliente pelo ID
    filme   = buscar_por_id(dados["filmes"], id_filme)
    cliente = buscar_por_id(dados["clientes"], id_cliente)

    # Validações
    if not filme:
        print("❌ Filme não encontrado."); return
    if not filme["disponivel"]:
        print("❌ Filme indisponível para venda."); return
    if not cliente:
        print("❌ Cliente não encontrado."); return

    # Registra a venda
    venda = {
        "id": novo_id(dados["vendas"]),
        "id_filme": id_filme,
        "titulo_filme": filme["titulo"],
        "id_cliente": id_cliente,
        "nome_cliente": cliente["nome"],
        "data": str(date.today()),
        "valor": valor
    }
    dados["vendas"].append(venda)

    # Filme vendido sai do catálogo
    filme["disponivel"] = False

    salvar(dados)
    print(f'\n✅ Venda #{venda["id"]} registrada! "{filme["titulo"]}" vendido para {cliente["nome"]}.')

def listar_vendas():
    dados  = carregar()
    vendas = dados["vendas"]

    if not vendas:
        print("\n⚠️  Nenhuma venda registrada.")
        return

    # Cabeçalho da tabela
    print(f'\n{"ID":<5} {"Filme":<25} {"Cliente":<20} {"Data":<12} {"Valor"}')
    print("-" * 70)

    for v in vendas:
        print(f'{v["id"]:<5} {v["titulo_filme"]:<25} {v["nome_cliente"]:<20} '
              f'{v["data"]:<12} R${v["valor"]:.2f}')
