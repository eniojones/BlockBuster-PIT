"""
Blockbuster PIT — Versão Streamlit
Execute com: streamlit run app.py
"""

import json
import os
from datetime import date
import streamlit as st

# ── CONFIGURAÇÃO DA PÁGINA ─────────────────────────────────────────────────
st.set_page_config(
    page_title="Blockbuster PIT",
    page_icon="🎬",
    layout="wide",
)

# ── ESTILO CUSTOMIZADO ─────────────────────────────────────────────────────
st.markdown("""
<style>
    [data-testid="stSidebar"] { background-color: #1a1a2e; }
    [data-testid="stSidebar"] * { color: #e0e0ff !important; }
    .titulo-secao { color: #e94560; font-size: 1.4rem; font-weight: bold; margin-bottom: 0.5rem; }
    .card-info { background: #16213e; border-radius: 10px; padding: 1rem; margin-bottom: 0.5rem; }
    div[data-testid="metric-container"] { background: #16213e; border-radius: 8px; padding: 0.5rem 1rem; }
</style>
""", unsafe_allow_html=True)

# ── DATABASE ───────────────────────────────────────────────────────────────
ARQUIVO = "dados.json"
BANCO_VAZIO = {"filmes": [], "clientes": [], "alugueis": [], "vendas": []}

def carregar():
    if not os.path.exists(ARQUIVO):
        salvar(BANCO_VAZIO)
        return BANCO_VAZIO
    with open(ARQUIVO, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar(dados):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)

def buscar_por_id(lista, id_alvo):
    return next((item for item in lista if item["id"] == id_alvo), None)

def novo_id(lista):
    return max((item["id"] for item in lista), default=0) + 1

# ── SIDEBAR ────────────────────────────────────────────────────────────────
st.sidebar.title("🎬 Blockbuster PIT")
st.sidebar.markdown("---")
pagina = st.sidebar.radio(
    "Navegação",
    ["🏠 Dashboard", "🎥 Filmes", "👤 Clientes", "📦 Aluguéis", "💰 Vendas"],
)
st.sidebar.markdown("---")
dados = carregar()
st.sidebar.metric("Filmes", len(dados["filmes"]))
st.sidebar.metric("Clientes", len(dados["clientes"]))
st.sidebar.metric("Aluguéis", len(dados["alugueis"]))
st.sidebar.metric("Vendas", len(dados["vendas"]))

# ══════════════════════════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════════════════════════
if pagina == "🏠 Dashboard":
    st.title("🎬 Blockbuster PIT — Dashboard")
    dados = carregar()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🎥 Filmes cadastrados", len(dados["filmes"]))
    col2.metric("👤 Clientes", len(dados["clientes"]))
    col3.metric("📦 Aluguéis ativos",
                sum(1 for a in dados["alugueis"] if not a.get("devolvido")))
    col4.metric("💰 Total em vendas",
                f"R$ {sum(v['valor'] for v in dados['vendas']):.2f}")

    st.markdown("---")
    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("📋 Últimos filmes cadastrados")
        filmes = dados["filmes"][-5:][::-1]
        if filmes:
            for f in filmes:
                disp = "✅ Disponível" if f["disponivel"] else "🔴 Indisponível"
                st.markdown(f"**{f['titulo']}** — {f['genero']} ({f['ano']}) — {disp}")
        else:
            st.info("Nenhum filme cadastrado ainda.")

    with col_b:
        st.subheader("📋 Últimos aluguéis")
        alugueis = dados["alugueis"][-5:][::-1]
        if alugueis:
            for a in alugueis:
                status = "✅ Devolvido" if a["devolvido"] else "⏳ Em aberto"
                st.markdown(f"**{a['titulo_filme']}** → {a['nome_cliente']} — {status}")
        else:
            st.info("Nenhum aluguel registrado ainda.")

# ══════════════════════════════════════════════════════════════════════════
# FILMES
# ══════════════════════════════════════════════════════════════════════════
elif pagina == "🎥 Filmes":
    st.title("🎥 Gerenciamento de Filmes")
    aba = st.tabs(["📋 Listar", "➕ Cadastrar", "✏️ Atualizar", "🗑️ Remover"])

    # ── Listar ──
    with aba[0]:
        dados = carregar()
        filmes = dados["filmes"]
        if not filmes:
            st.info("Nenhum filme cadastrado.")
        else:
            busca = st.text_input("🔍 Buscar por título", "")
            resultado = [f for f in filmes if busca.lower() in f["titulo"].lower()]
            for f in resultado:
                disp = "✅ Disponível" if f["disponivel"] else "🔴 Indisponível"
                with st.expander(f"#{f['id']} — {f['titulo']} ({f['ano']})"):
                    st.write(f"**Gênero:** {f['genero']}")
                    st.write(f"**Status:** {disp}")

    # ── Cadastrar ──
    with aba[1]:
        with st.form("form_criar_filme"):
            st.subheader("Novo filme")
            titulo  = st.text_input("Título *")
            genero  = st.text_input("Gênero (Ex: Ação, Terror...)")
            ano     = st.text_input("Ano de lançamento")
            submit  = st.form_submit_button("💾 Cadastrar")

        if submit:
            if not titulo.strip():
                st.error("O título é obrigatório!")
            else:
                dados = carregar()
                filme = {
                    "id": novo_id(dados["filmes"]),
                    "titulo": titulo.strip(),
                    "genero": genero.strip(),
                    "ano": ano.strip(),
                    "disponivel": True,
                }
                dados["filmes"].append(filme)
                salvar(dados)
                st.success(f'Filme "{titulo}" cadastrado com sucesso! ID: {filme["id"]}')

    # ── Atualizar ──
    with aba[2]:
        dados = carregar()
        if not dados["filmes"]:
            st.info("Nenhum filme cadastrado.")
        else:
            opcoes = {f["id"]: f"#{f['id']} — {f['titulo']}" for f in dados["filmes"]}
            id_sel = st.selectbox("Selecione o filme", list(opcoes.keys()),
                                  format_func=lambda x: opcoes[x])
            filme = buscar_por_id(dados["filmes"], id_sel)
            if filme:
                with st.form("form_atualizar_filme"):
                    titulo_novo  = st.text_input("Título",  value=filme["titulo"])
                    genero_novo  = st.text_input("Gênero",  value=filme["genero"])
                    ano_novo     = st.text_input("Ano",     value=filme["ano"])
                    submit_upd   = st.form_submit_button("💾 Salvar alterações")
                if submit_upd:
                    filme["titulo"] = titulo_novo.strip() or filme["titulo"]
                    filme["genero"] = genero_novo.strip() or filme["genero"]
                    filme["ano"]    = ano_novo.strip()    or filme["ano"]
                    salvar(dados)
                    st.success("Filme atualizado!")

    # ── Remover ──
    with aba[3]:
        dados = carregar()
        if not dados["filmes"]:
            st.info("Nenhum filme cadastrado.")
        else:
            opcoes = {f["id"]: f"#{f['id']} — {f['titulo']}" for f in dados["filmes"]}
            id_del = st.selectbox("Selecione o filme a remover", list(opcoes.keys()),
                                  format_func=lambda x: opcoes[x])
            if st.button("🗑️ Remover filme", type="primary"):
                dados["filmes"] = [f for f in dados["filmes"] if f["id"] != id_del]
                salvar(dados)
                st.success("Filme removido!")
                st.rerun()

# ══════════════════════════════════════════════════════════════════════════
# CLIENTES
# ══════════════════════════════════════════════════════════════════════════
elif pagina == "👤 Clientes":
    st.title("👤 Gerenciamento de Clientes")
    aba = st.tabs(["📋 Listar", "➕ Cadastrar", "✏️ Atualizar", "🗑️ Remover"])

    with aba[0]:
        dados = carregar()
        clientes = dados["clientes"]
        if not clientes:
            st.info("Nenhum cliente cadastrado.")
        else:
            busca = st.text_input("🔍 Buscar por nome", "")
            resultado = [c for c in clientes if busca.lower() in c["nome"].lower()]
            for c in resultado:
                with st.expander(f"#{c['id']} — {c['nome']}"):
                    st.write(f"**CPF:** {c['cpf']}")
                    st.write(f"**Telefone:** {c['telefone']}")

    with aba[1]:
        with st.form("form_criar_cliente"):
            st.subheader("Novo cliente")
            nome      = st.text_input("Nome *")
            cpf       = st.text_input("CPF")
            telefone  = st.text_input("Telefone")
            submit    = st.form_submit_button("💾 Cadastrar")

        if submit:
            if not nome.strip():
                st.error("O nome é obrigatório!")
            else:
                dados = carregar()
                cliente = {
                    "id": novo_id(dados["clientes"]),
                    "nome": nome.strip(),
                    "cpf": cpf.strip(),
                    "telefone": telefone.strip(),
                }
                dados["clientes"].append(cliente)
                salvar(dados)
                st.success(f'Cliente "{nome}" cadastrado! ID: {cliente["id"]}')

    with aba[2]:
        dados = carregar()
        if not dados["clientes"]:
            st.info("Nenhum cliente cadastrado.")
        else:
            opcoes = {c["id"]: f"#{c['id']} — {c['nome']}" for c in dados["clientes"]}
            id_sel = st.selectbox("Selecione o cliente", list(opcoes.keys()),
                                  format_func=lambda x: opcoes[x])
            cliente = buscar_por_id(dados["clientes"], id_sel)
            if cliente:
                with st.form("form_atualizar_cliente"):
                    nome_novo      = st.text_input("Nome",     value=cliente["nome"])
                    cpf_novo       = st.text_input("CPF",      value=cliente["cpf"])
                    telefone_novo  = st.text_input("Telefone", value=cliente["telefone"])
                    submit_upd     = st.form_submit_button("💾 Salvar alterações")
                if submit_upd:
                    cliente["nome"]     = nome_novo.strip()     or cliente["nome"]
                    cliente["cpf"]      = cpf_novo.strip()      or cliente["cpf"]
                    cliente["telefone"] = telefone_novo.strip() or cliente["telefone"]
                    salvar(dados)
                    st.success("Cliente atualizado!")

    with aba[3]:
        dados = carregar()
        if not dados["clientes"]:
            st.info("Nenhum cliente cadastrado.")
        else:
            opcoes = {c["id"]: f"#{c['id']} — {c['nome']}" for c in dados["clientes"]}
            id_del = st.selectbox("Selecione o cliente a remover", list(opcoes.keys()),
                                  format_func=lambda x: opcoes[x])
            if st.button("🗑️ Remover cliente", type="primary"):
                dados["clientes"] = [c for c in dados["clientes"] if c["id"] != id_del]
                salvar(dados)
                st.success("Cliente removido!")
                st.rerun()

# ══════════════════════════════════════════════════════════════════════════
# ALUGUÉIS
# ══════════════════════════════════════════════════════════════════════════
elif pagina == "📦 Aluguéis":
    st.title("📦 Gerenciamento de Aluguéis")
    aba = st.tabs(["📋 Listar", "➕ Registrar aluguel", "↩️ Registrar devolução"])

    with aba[0]:
        dados = carregar()
        alugueis = dados["alugueis"]
        if not alugueis:
            st.info("Nenhum aluguel registrado.")
        else:
            filtro = st.selectbox("Filtrar", ["Todos", "Em aberto", "Devolvidos"])
            if filtro == "Em aberto":
                alugueis = [a for a in alugueis if not a["devolvido"]]
            elif filtro == "Devolvidos":
                alugueis = [a for a in alugueis if a["devolvido"]]
            for a in alugueis[::-1]:
                status = "✅ Devolvido" if a["devolvido"] else "⏳ Em aberto"
                with st.expander(f"#{a['id']} — {a['titulo_filme']} → {a['nome_cliente']} — {status}"):
                    col1, col2, col3 = st.columns(3)
                    col1.write(f"**Data:** {a['data']}")
                    col2.write(f"**Dias:** {a['dias']}")
                    col3.write(f"**Valor:** R$ {a['valor']:.2f}")

    with aba[1]:
        dados = carregar()
        filmes_disp = [f for f in dados["filmes"] if f["disponivel"]]
        clientes    = dados["clientes"]

        if not filmes_disp:
            st.warning("Nenhum filme disponível para aluguel.")
        elif not clientes:
            st.warning("Nenhum cliente cadastrado.")
        else:
            with st.form("form_aluguel"):
                st.subheader("Novo aluguel")
                op_filmes   = {f["id"]: f"#{f['id']} — {f['titulo']}" for f in filmes_disp}
                op_clientes = {c["id"]: f"#{c['id']} — {c['nome']}"   for c in clientes}
                id_filme    = st.selectbox("Filme", list(op_filmes.keys()),
                                           format_func=lambda x: op_filmes[x])
                id_cliente  = st.selectbox("Cliente", list(op_clientes.keys()),
                                           format_func=lambda x: op_clientes[x])
                dias        = st.number_input("Quantidade de dias", min_value=1, value=3)
                valor       = st.number_input("Valor do aluguel (R$)", min_value=0.0,
                                              value=5.0, step=0.5, format="%.2f")
                submit      = st.form_submit_button("💾 Registrar aluguel")

            if submit:
                dados   = carregar()
                filme   = buscar_por_id(dados["filmes"],   id_filme)
                cliente = buscar_por_id(dados["clientes"], id_cliente)
                aluguel = {
                    "id":            novo_id(dados["alugueis"]),
                    "id_filme":      id_filme,
                    "titulo_filme":  filme["titulo"],
                    "id_cliente":    id_cliente,
                    "nome_cliente":  cliente["nome"],
                    "data":          str(date.today()),
                    "dias":          int(dias),
                    "valor":         float(valor),
                    "devolvido":     False,
                }
                dados["alugueis"].append(aluguel)
                filme["disponivel"] = False
                salvar(dados)
                st.success(f'Aluguel #{aluguel["id"]} registrado! '
                           f'"{filme["titulo"]}" para {cliente["nome"]}.')

    with aba[2]:
        dados = carregar()
        em_aberto = [a for a in dados["alugueis"] if not a["devolvido"]]
        if not em_aberto:
            st.info("Nenhum aluguel em aberto.")
        else:
            opcoes = {a["id"]: f"#{a['id']} — {a['titulo_filme']} ({a['nome_cliente']})"
                      for a in em_aberto}
            id_dev = st.selectbox("Selecione o aluguel", list(opcoes.keys()),
                                  format_func=lambda x: opcoes[x])
            if st.button("↩️ Confirmar devolução", type="primary"):
                dados   = carregar()
                aluguel = buscar_por_id(dados["alugueis"], id_dev)
                aluguel["devolvido"] = True
                filme = buscar_por_id(dados["filmes"], aluguel["id_filme"])
                if filme:
                    filme["disponivel"] = True
                salvar(dados)
                st.success(f"Devolução do aluguel #{id_dev} registrada!")
                st.rerun()

# ══════════════════════════════════════════════════════════════════════════
# VENDAS
# ══════════════════════════════════════════════════════════════════════════
elif pagina == "💰 Vendas":
    st.title("💰 Gerenciamento de Vendas")
    aba = st.tabs(["📋 Listar", "➕ Registrar venda"])

    with aba[0]:
        dados = carregar()
        vendas = dados["vendas"]
        if not vendas:
            st.info("Nenhuma venda registrada.")
        else:
            total = sum(v["valor"] for v in vendas)
            st.metric("💵 Total arrecadado", f"R$ {total:.2f}")
            st.markdown("---")
            for v in vendas[::-1]:
                with st.expander(f"#{v['id']} — {v['titulo_filme']} → {v['nome_cliente']}"):
                    col1, col2 = st.columns(2)
                    col1.write(f"**Data:** {v['data']}")
                    col2.write(f"**Valor:** R$ {v['valor']:.2f}")

    with aba[1]:
        dados = carregar()
        filmes_disp = [f for f in dados["filmes"] if f["disponivel"]]
        clientes    = dados["clientes"]

        if not filmes_disp:
            st.warning("Nenhum filme disponível para venda.")
        elif not clientes:
            st.warning("Nenhum cliente cadastrado.")
        else:
            with st.form("form_venda"):
                st.subheader("Nova venda")
                op_filmes   = {f["id"]: f"#{f['id']} — {f['titulo']}" for f in filmes_disp}
                op_clientes = {c["id"]: f"#{c['id']} — {c['nome']}"   for c in clientes}
                id_filme    = st.selectbox("Filme", list(op_filmes.keys()),
                                           format_func=lambda x: op_filmes[x])
                id_cliente  = st.selectbox("Cliente", list(op_clientes.keys()),
                                           format_func=lambda x: op_clientes[x])
                valor       = st.number_input("Valor da venda (R$)", min_value=0.0,
                                              value=20.0, step=1.0, format="%.2f")
                submit      = st.form_submit_button("💾 Registrar venda")

            if submit:
                dados   = carregar()
                filme   = buscar_por_id(dados["filmes"],   id_filme)
                cliente = buscar_por_id(dados["clientes"], id_cliente)
                venda   = {
                    "id":           novo_id(dados["vendas"]),
                    "id_filme":     id_filme,
                    "titulo_filme": filme["titulo"],
                    "id_cliente":   id_cliente,
                    "nome_cliente": cliente["nome"],
                    "data":         str(date.today()),
                    "valor":        float(valor),
                }
                dados["vendas"].append(venda)
                filme["disponivel"] = False
                salvar(dados)
                st.success(f'Venda #{venda["id"]} registrada! '
                           f'"{filme["titulo"]}" para {cliente["nome"]}.')
