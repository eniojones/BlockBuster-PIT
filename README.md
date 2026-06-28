# Locadora Blockbuster — Python

Projeto desenvolvido para a disciplina de **Algoritmos e Programação** do 1º período do curso de **Bacharelado em Inteligência Artificial** do Piauí Instituto de Tecnologia (PIT).

---

## Descrição do Projeto

O sistema tem como objetivo realizar o **gerenciamento de uma locadora de filmes**, permitindo o armazenamento permanente dos dados por meio de arquivos JSON.

O software implementa um **CRUD completo** (Create, Read, Update e Delete) utilizando listas de dicionários para armazenar informações de filmes, clientes, aluguéis e vendas, aplicando os conceitos estudados durante a disciplina.

---

## Funcionalidades

- **Filmes:** cadastrar, listar, atualizar e remover filmes do catálogo
- **Clientes:** cadastrar, listar, atualizar e remover clientes
- **Aluguéis:** registrar aluguéis, listar e registrar devoluções
- **Vendas:** registrar e listar vendas de filmes
- **Persistência de Dados:** todas as informações são armazenadas no arquivo `dados.json`, garantindo que os dados permaneçam disponíveis mesmo após o encerramento da aplicação

---

## Tecnologias Utilizadas

- **Linguagem:** Python 3
- **Biblioteca `json`:** nativa do Python, usada para serialização e persistência de dados
- **Biblioteca `datetime`:** nativa do Python, usada para registrar automaticamente a data dos aluguéis e vendas

---

## Estrutura do Projeto

```
Blockbuster/
│
├── database.py   → Funções de carregar, salvar e buscar dados (reutilizadas em todo o projeto)
├── clientes.py   → CRUD de clientes
├── filmes.py     → CRUD de filmes
├── alugueis.py   → Registro de aluguéis e devoluções
├── vendas.py     → Registro de vendas
├── main.py       → Menu principal e navegação do sistema
└── dados.json    → Banco de dados gerado automaticamente na primeira execução
```

O sistema foi organizado de forma **modular** para facilitar a manutenção e a reutilização do código, separando claramente as responsabilidades de cada arquivo.

---

## Como Executar

```bash
python main.py
```

> Certifique-se de ter o **Python 3.8 ou superior** instalado.

---

## Técnicas e Conceitos Aplicados

Abaixo estão todos os conceitos de Python utilizados no projeto, com exemplos de código, links para a documentação oficial e vídeos explicativos no YouTube.

---

### 1. Princípio DRY — Não Repita Código

**O que é:**
DRY significa *Don't Repeat Yourself* (Não Se Repita). Sempre que um trecho de código se repete em vários lugares, ele deve virar uma função reutilizável. Isso torna o código mais fácil de manter e corrigir.

**Como foi aplicado:**
As funções `buscar_por_id()` e `novo_id()` foram criadas no `database.py` e importadas em todos os outros arquivos, eliminando repetição.

```python
# database.py — funções criadas uma vez e usadas em todo o projeto
def buscar_por_id(lista, id_alvo):
    return next((item for item in lista if item["id"] == id_alvo), None)

def novo_id(lista):
    return max((item["id"] for item in lista), default=0) + 1
```

**Documentação Python — Funções:**
https://docs.python.org/pt-br/3/tutorial/functions.html

**Vídeo — Funções em Python (def, parâmetros e retorno):**
https://www.youtube.com/watch?v=CSWx1Mr2xms

**Vídeo — Como criar funções em Python (iniciantes):**
https://www.youtube.com/watch?v=mb5OeMveUzg

---

### 2. Função `next()` com Generator Expression

**O que é:**
`next()` percorre uma lista e retorna o **primeiro item** que satisfaz uma condição, sem precisar de um `for` com `if` aninhado. O segundo parâmetro (`None`) é o valor retornado caso nenhum item seja encontrado.

**Como foi aplicado:**

```python
# Antes — for com if aninhado
for c in dados["clientes"]:
    if c["id"] == id_alvo:
        # faz algo com c

# Depois — uma única linha
cliente = next((c for c in dados["clientes"] if c["id"] == id_alvo), None)
```

**Documentação Python — `next()`:**
https://docs.python.org/pt-br/3/library/functions.html#next

**Documentação Python — Expressões Geradoras:**
https://docs.python.org/pt-br/3/tutorial/classes.html#generator-expressions

**Vídeo — List Comprehension e Generator Expressions (PT-BR):**
https://www.youtube.com/watch?v=ElX6dOSd1xw

---

### 3. List Comprehension — Filtrar Listas

**O que é:**
List Comprehension é uma forma compacta de criar uma nova lista filtrando ou transformando os itens de outra lista, em uma única linha. É amplamente usada em Python por ser mais legível e eficiente que o `for` tradicional.

**Como foi aplicado:**
Usado para remover clientes e filmes — cria uma nova lista com todos os itens, exceto o que deve ser removido.

```python
# Antes
clientes_novos = []
for c in dados["clientes"]:
    if c["id"] != id_alvo:
        clientes_novos.append(c)
dados["clientes"] = clientes_novos

# Depois
dados["clientes"] = [c for c in original if c["id"] != id_alvo]
```

**Documentação Python — List Comprehension:**
https://docs.python.org/pt-br/3/tutorial/datastructures.html#list-comprehensions

**Vídeo — O que é List Comprehension? (PT-BR):**
https://www.youtube.com/watch?v=ElX6dOSd1xw

**Vídeo — List Comprehension no Python (Hashtag Treinamentos):**
https://www.youtube.com/watch?v=M2zL6LnQwkw

---

### 4. f-strings — Formatação de Texto

**O que é:**
f-strings permitem inserir variáveis diretamente dentro de textos de forma simples e legível. O `:< 25` define o alinhamento à esquerda e reserva 25 caracteres de espaço, garantindo que as tabelas fiquem alinhadas.

**Como foi aplicado:**
Corrigimos um bug onde `{'disponivel'}` imprimia o texto literal em vez do valor da variável, e padronizamos o cabeçalho de todas as tabelas.

```python
# Bug — imprimia "disponivel" como texto literal
print(f"... {'disponivel'}")

# Correto — imprime o valor da variável
disponivel = "Sim" if f["disponivel"] else "Não"
print(f'{f["id"]:<5} {f["titulo"]:<25} {disponivel}')
```

**Documentação Python — f-strings:**
https://docs.python.org/pt-br/3/tutorial/inputoutput.html#formatted-string-literals

**Vídeo — Como usar f-strings em Python:**
https://www.youtube.com/watch?v=x-UsB5PzsX4

**Vídeo — F-strings: a melhor forma de formatar strings:**
https://www.youtube.com/watch?v=zjOoUkU-WjM

---

### 5. `try / except` — Tratamento de Erros

**O que é:**
`try / except` evita que o programa encerre inesperadamente quando o usuário digita algo inválido (como letras no lugar de números). O `ValueError` é o tipo de erro lançado quando uma conversão de tipo falha.

**Como foi aplicado:**
Utilizado em todas as funções que recebem entrada numérica do usuário.

```python
try:
    id_alvo = int(input("ID do cliente: "))
except ValueError:
    print("ID inválido.")
    return
```

**Documentação Python — Tratamento de Exceções:**
https://docs.python.org/pt-br/3/tutorial/errors.html#handling-exceptions

**Vídeo — Try Except — Tratamento de Erros - Curso Python #26:**
https://www.youtube.com/watch?v=jT-C3OjUBvQ

**Vídeo — Try e Except no Python (Hashtag Treinamentos):**
https://www.youtube.com/watch?v=h01u7A3lWZY

---

### 6. Dicionários como Dispatcher — Menu

**O que é:**
Em vez de vários `elif` para cada opção do menu, usamos um dicionário onde cada chave é uma opção e o valor é a função a ser chamada. Isso torna o código mais limpo e fácil de expandir.

**Como foi aplicado:**
A função `executar_menu()` foi criada para centralizar a lógica de todos os menus, e o `main()` passou a usar um dicionário para chamar o menu correto.

```python
# Antes — elif repetido para cada opção
elif escolha == "1": menu_filmes()
elif escolha == "2": menu_clientes()
elif escolha == "3": menu_alugueis()
elif escolha == "4": menu_vendas()

# Depois — dicionário + uma linha
menus = {"1": menu_filmes, "2": menu_clientes, "3": menu_alugueis, "4": menu_vendas}
if escolha in menus:
    menus[escolha]()
```

**Documentação Python — Dicionários:**
https://docs.python.org/pt-br/3/tutorial/datastructures.html#dictionaries

**Vídeo — Dicionários em Python (Hashtag Treinamentos):**
https://www.youtube.com/watch?v=M2zL6LnQwkw

---

### 7. `max()` com `default` — Geração de ID Automático

**O que é:**
`max()` retorna o maior valor de uma lista. O parâmetro `default=0` evita erro quando a lista está vazia (nenhum item cadastrado ainda), retornando `0` como valor padrão, e então somamos `+1` para gerar o próximo ID.

**Como foi aplicado:**

```python
def novo_id(lista):
    return max((item["id"] for item in lista), default=0) + 1
```

**Documentação Python — `max()`:**
https://docs.python.org/pt-br/3/library/functions.html#max

---

### 8. `date.today()` — Data Automática

**O que é:**
`date.today()` do módulo `datetime` retorna a data atual do sistema automaticamente, sem precisar que o usuário a informe manualmente.

**Como foi aplicado:**

```python
from datetime import date

aluguel = {
    "data": str(date.today())  # Ex: "2026-06-04"
}
```

**Documentação Python — `datetime.date`:**
https://docs.python.org/pt-br/3/library/datetime.html#datetime.date.today

---

## Desafios Encontrados

Durante o desenvolvimento, os principais desafios foram:

- **Remoção segura de itens:** garantir que ao deletar um cliente ou filme, a lista fosse recriada corretamente sem afetar os outros registros
- **Verificação de existência do arquivo JSON:** tratar adequadamente a situação em que o arquivo `dados.json` ainda não existia na primeira execução
- **Bugs nas f-strings:** identificar e corrigir casos onde variáveis dentro de f-strings estavam sendo impressas como texto literal ao invés de seus valores
- **Inconsistência nas chaves dos dicionários:** corrigir diferenças de capitalização (`'Id'` vs `'id'`, `'Nome'` vs `'nome'`) que causavam erros em tempo de execução

---

## Uso de Inteligência Artificial

A Inteligência Artificial foi utilizada como ferramenta de apoio ao desenvolvimento do projeto, auxiliando em:

1. Geração de comentários explicativos no código para facilitar o entendimento
2. Identificação e correção de bugs nas f-strings e nas chaves dos dicionários
3. Conversão do sistema original (terminal) para uma interface web utilizando a biblioteca **Streamlit**

### Prompt utilizado para conversão ao Streamlit

> *"Adapte esse código para o Streamlit"*
> — enviado junto com o link do repositório: https://github.com/eniojones/BlockBuster-PIT

**Ferramenta utilizada:** Claude (Anthropic) — [claude.ai](https://claude.ai)

**O que a IA fez a partir desse prompt:**
- Leu todos os arquivos do repositório (`database.py`, `filmes.py`, `clientes.py`, `alugueis.py`, `vendas.py`)
- Unificou os módulos em um único arquivo `app.py`
- Substituiu os menus de terminal (`input()` / `print()`) por componentes visuais do Streamlit: sidebar, abas, formulários, botões e métricas
- Adicionou um Dashboard com visão geral do sistema
- Manteve toda a lógica original de persistência com `dados.json` sem alterações


---

## Equipe

- Enio Jones Porto
- Ana Catharina
- Wellison Samuel

---

## Materiais da Disciplina (PIT)

- Fundamentos de Lógica e Python
- Estruturas Condicionais
- Estruturas de Repetição
- Manipulação de Listas
- Funções e Modularização
- Uso de Bibliotecas
- Dicionários e Listas de Dicionários
- Persistência de Arquivos e JSON

---

## Referências Técnicas

| Tema | Documentação Oficial | Vídeo YouTube |
|---|---|---|
| Funções (`def`) | [docs.python.org](https://docs.python.org/pt-br/3/tutorial/functions.html) | [Funções em Python](https://www.youtube.com/watch?v=CSWx1Mr2xms) |
| List Comprehension | [docs.python.org](https://docs.python.org/pt-br/3/tutorial/datastructures.html#list-comprehensions) | [List Comprehension](https://www.youtube.com/watch?v=ElX6dOSd1xw) |
| `next()` | [docs.python.org](https://docs.python.org/pt-br/3/library/functions.html#next) | [List Comprehension](https://www.youtube.com/watch?v=ElX6dOSd1xw) |
| f-strings | [docs.python.org](https://docs.python.org/pt-br/3/tutorial/inputoutput.html#formatted-string-literals) | [f-strings em Python](https://www.youtube.com/watch?v=x-UsB5PzsX4) |
| `try / except` | [docs.python.org](https://docs.python.org/pt-br/3/tutorial/errors.html) | [Try e Except](https://www.youtube.com/watch?v=jT-C3OjUBvQ) |
| Dicionários | [docs.python.org](https://docs.python.org/pt-br/3/tutorial/datastructures.html#dictionaries) | [Dicionários](https://www.youtube.com/watch?v=M2zL6LnQwkw) |
| `max()` | [docs.python.org](https://docs.python.org/pt-br/3/library/functions.html#max) | — |
| `datetime` | [docs.python.org](https://docs.python.org/pt-br/3/library/datetime.html) | — |
| Princípio DRY | [Alura Língua](https://www.aluralingua.com.br/artigos/voce-conhece-o-principio-dry-em-programacao) | [Funções em Python](https://www.youtube.com/watch?v=CSWx1Mr2xms) |
| JSON em Python | [docs.python.org](https://docs.python.org/pt-br/3/library/json.html) | [Formatação de Strings](https://www.youtube.com/watch?v=x-UsB5PzsX4) |

---

## Documentação Oficial Python (Português)

https://docs.python.org/pt-br/3/

---

*Projeto desenvolvido para fins educacionais — Disciplina de Algoritmos e Programação — PIT 2026.*
