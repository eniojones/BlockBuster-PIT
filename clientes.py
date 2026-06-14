from database import carregar, salvar, buscar_por_id, novo_id

def criar_cliente():
    dados = carregar()

    nome     = input("Nome do cliente: ").strip()
    cpf      = input("CPF: ").strip()
    telefone = input("Telefone: ").strip()

    cliente = {
        "id": novo_id(dados["clientes"]),
        "nome": nome,
        "cpf": cpf,
        "telefone": telefone
    }
    dados["clientes"].append(cliente)

    salvar(dados)
    print(f'\nCliente "{nome}" cadastrado com o ID {cliente["id"]}!')

def listar_clientes():
    dados    = carregar()
    clientes = dados["clientes"]

    if not clientes:
        print("\nNenhum cliente cadastrado.")
        return

    print(f'\n{"ID":<5} {"Nome":<25} {"CPF":<15} {"Telefone"}')
    print("-" * 55)

    for c in clientes:
        print(f'{c["id"]:<5} {c["nome"]:<25} {c["cpf"]:<15} {c["telefone"]}')

def atualizar_cliente():
    listar_clientes()

    try:
        id_alvo = int(input("\nID do cliente a atualizar: "))
    except ValueError:
        print("ID inválido.")
        return

    dados   = carregar()
    cliente = buscar_por_id(dados["clientes"], id_alvo)

    if not cliente:
        print("Cliente não encontrado.")
        return

    for campo in ["nome", "cpf", "telefone"]:
        valor = input(f"{campo.capitalize()} [{cliente[campo]}]: ").strip()
        if valor:
            cliente[campo] = valor

    salvar(dados)
    print("Cliente atualizado!")

def deletar_cliente():
    listar_clientes()

    try:
        id_alvo = int(input("\nID do cliente a remover: "))
    except ValueError:
        print("ID inválido.")
        return

    dados    = carregar()
    original = dados["clientes"]

    dados["clientes"] = [c for c in original if c["id"] != id_alvo]

    if len(dados["clientes"]) == len(original):
        print("Cliente não encontrado.")
        return

    salvar(dados)
    print("Cliente removido!")
