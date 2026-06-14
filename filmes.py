from database import carregar, salvar, buscar_por_id, novo_id

def criar_filme():
    dados = carregar()

    titulo = input("Título do filme: ").strip()
    genero = input("Gênero (Ex: Ação, Terror...): ").strip()
    ano    = input("Ano de lançamento: ").strip()

    filme = {
        "id": novo_id(dados["filmes"]),
        "titulo": titulo,
        "genero": genero,
        "ano": ano,
        "disponivel": True
    }
    dados["filmes"].append(filme)

    salvar(dados)
    print(f'\nFilme "{titulo}" cadastrado com sucesso! ID: {filme["id"]}')

def listar_filmes():
    dados  = carregar()
    filmes = dados["filmes"]

    if not filmes:
        print("\nNenhum filme cadastrado.")
        return

    print(f'\n{"ID":<5} {"Título":<25} {"Gênero":<15} {"Ano":<6} {"Disponível"}')
    print("-" * 65)

    for f in filmes:
        disponivel = "Sim" if f["disponivel"] else "Não"
        print(f'{f["id"]:<5} {f["titulo"]:<25} {f["genero"]:<15} {f["ano"]:<6} {disponivel}')

def atualizar_filme():
    listar_filmes()

    try:
        id_alvo = int(input("\nID do filme a atualizar: "))
    except ValueError:
        print("ID inválido!")
        return

    dados = carregar()
    filme = buscar_por_id(dados["filmes"], id_alvo)

    if not filme:
        print("Filme não encontrado.")
        return

    for campo in ["titulo", "genero", "ano"]:
        valor = input(f"{campo.capitalize()} [{filme[campo]}]: ").strip()
        if valor:
            filme[campo] = valor

    salvar(dados)
    print("Filme atualizado!")

def deletar_filme():
    listar_filmes()

    try:
        id_alvo = int(input("\nID do filme a remover: "))
    except ValueError:
        print("ID inválido!")
        return

    dados    = carregar()
    original = dados["filmes"]

    dados["filmes"] = [f for f in original if f["id"] != id_alvo]

    if len(dados["filmes"]) == len(original):
        print("Filme não encontrado.")
        return

    salvar(dados)
    print("Filme removido!")
