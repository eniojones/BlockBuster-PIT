from database import carregar, salvar, buscar_por_id, novo_id

def criar_filme():
    dados = carregar()

    # Pede os dados do novo filme
    titulo = input("Título do filme: ").strip()
    genero = input("Gênero (Ex: Ação, Terror...): ").strip()
    ano    = input("Ano de lançamento: ").strip()

    # Cria o filme e adiciona na lista
    filme = {
        "id": novo_id(dados["filmes"]),
        "titulo": titulo,
        "genero": genero,
        "ano": ano,
        "disponivel": True  # Todo filme começa disponível
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

    # Cabeçalho da tabela
    print(f'\n{"ID":<5} {"Título":<25} {"Gênero":<15} {"Ano":<6} {"Disponível"}')
    print("-" * 65)

    # Imprime cada filme formatado em colunas
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

    # Para cada campo, pergunta o novo valor
    # Se deixar em branco, mantém o valor atual
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

    # Cria nova lista sem o filme com o ID informado
    dados["filmes"] = [f for f in original if f["id"] != id_alvo]

    # Se o tamanho não mudou, o filme não foi encontrado
    if len(dados["filmes"]) == len(original):
        print("Filme não encontrado.")
        return

    salvar(dados)
    print("Filme removido!")
