import json
import os

ARQUIVO = "dados.json"

BANCO_VAZIO = {
    "filmes": [],
    "clientes": [],
    "alugueis": [],
    "vendas": []
}

def salvar(dados):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)

def carregar():
    if not os.path.exists(ARQUIVO):
        salvar(BANCO_VAZIO)
        return BANCO_VAZIO

    with open(ARQUIVO, "r", encoding="utf-8") as f:
        return json.load(f)

def buscar_por_id(lista, id_alvo):
    return next((item for item in lista if item["id"] == id_alvo), None)

def novo_id(lista):
    return max((item["id"] for item in lista), default=0) + 1
