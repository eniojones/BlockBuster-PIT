import json
import os

# Nome do arquivo onde os dados ficam salvos
ARQUIVO = "dados.json"

# Estrutura inicial do banco de dados (usado só na primeira vez)
BANCO_VAZIO = {
    "filmes": [],
    "clientes": [],
    "alugueis": [],
    "vendas": []
}

def salvar(dados):
    # Abre o arquivo e salva os dados no formato JSON
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)

def carregar():
    # Se o arquivo ainda não existe, cria um novo com o banco vazio
    if not os.path.exists(ARQUIVO):
        salvar(BANCO_VAZIO)
        return BANCO_VAZIO

    # Abre o arquivo e retorna os dados
    with open(ARQUIVO, "r", encoding="utf-8") as f:
        return json.load(f)

def buscar_por_id(lista, id_alvo):
    # Percorre a lista e retorna o item com o ID procurado
    # Retorna None se não encontrar nada
    return next((item for item in lista if item["id"] == id_alvo), None)

def novo_id(lista):
    # Gera um novo ID automático (pega o maior ID existente e soma 1)
    return max((item["id"] for item in lista), default=0) + 1
