# pages/5_Analise_SQL.py
# -*- coding: utf-8 -*-

import io
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
import base64

# --- FUNÇÃO DE BACKGROUND ---
    
def set_background_image_with_blur(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    st.markdown(
        f"""
        <style>
        [data-testid="stAppViewContainer"] {{
            position: relative;
            z-index: 0;
        }}
        [data-testid="stAppViewContainer"]::before {{
            content: "";
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: center;
            filter: blur(8px) brightness(0.5);
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
    
    
set_background_image_with_blur("BackGround/Dasa.png")

st.set_page_config(page_title="Análise via Oracle | Estoque Inteligente", page_icon="🗄️", layout="wide")
st.title("🗄️ Análise da Tabela de Insumos (Oracle)")

# =========================
# Lê credenciais (opcional)
# =========================
def read_secrets():
    try:
        sec = st.secrets["oracle"]
        return {
            "host": sec.get("host", "oracle.fiap.com.br"),
            "port": int(sec.get("port", 1521)),
            "service": sec.get("service", "ORCL"),
            "user": sec.get("user", "rm556055"),
            "password": sec.get("password", ""),
            "schema": sec.get("schema", "RM556055"),
            "use_sid": bool(sec.get("use_sid", False)),
        }
    except Exception:
        return None

defaults = read_secrets()

# =========================
# UI de conexão (Oracle)
# =========================
with st.expander("⚙️ Conexão ao Oracle", expanded=(defaults is None)):
    c1, c2, c3 = st.columns([1, 0.6, 0.6])
    host = c1.text_input("Host", value=(defaults["host"] if defaults else "oracle.fiap.com.br"))
    port = c2.number_input("Porta", value=(defaults["port"] if defaults else 1521), step=1)
    modo = c3.selectbox("Modo", ["Service Name (padrão)", "SID"],
                        index=(1 if (defaults and defaults.get("use_sid")) else 0))

    if modo.startswith("Service"):
        service = st.text_input("Service Name", value=(defaults["service"] if defaults else "ORCL"))
        sid = None
    else:
        sid = st.text_input("SID", value=(defaults["service"] if defaults else "ORCL"))
        service = None

    c4, c5, c6 = st.columns([0.7, 0.7, 0.7])
    user = c4.text_input("Usuário", value=(defaults["user"] if defaults else "rm556055"))
    password = c5.text_input("Senha", type="password", value=(defaults["password"] if defaults else ""))
    schema = c6.text_input("Schema (OWNER)", value=(defaults["schema"] if defaults else "RM556055")).strip().upper()

st.caption("Dica: use `.streamlit/secrets.toml` para salvar as credenciais (seção [oracle]).")

# =========================
# Conexão & consulta
# =========================
def _connect(_host, _port, _service, _sid, _user, _password):
    import oracledb
    if _sid:
        dsn = oracledb.makedsn(_host, int(_port), sid=_sid)
    else:
        dsn = f"{_host}:{int(_port)}/{_service}"
    return oracledb.connect(user=_user, password=_password, dsn=dsn)

@st.cache_data(show_spinner=True)
def query_insumos(_host, _port, _service, _sid, _user, _password, _schema):
    import oracledb
    conn = _connect(_host, _port, _service, _sid, _user, _password)
    sql = f"""
        SELECT
            INSUMO,
            QUANTIDADE,
            EXAME
        FROM {_schema}.INSUMOS
    """
    df = pd.read_sql(sql, conn)
    conn.close()

    # Normalização robusta
    df.columns = [str(c).upper().strip() for c in df.columns]

    if "QUANTIDADE" in df.columns:
        df["QUANTIDADE"] = pd.to_numeric(df["QUANTIDADE"], errors="coerce").fillna(0).astype(int)

    for c in ("INSUMO", "EXAME"):
        if c in df.columns:
            df[c] = df[c].astype("string").fillna("").str.strip()

    return df

# -------------------------
# Botões de ação
# -------------------------
b1, b2 = st.columns([0.5, 0.5])
conectar = b1.button("🔌 Conectar e carregar do Oracle", use_container_width=True)
recarregar = b2.button("🔄 Atualizar (limpar cache e ler novamente)", use_container_width=True)

if recarregar:
    query_insumos.clear()
    st.session_state.pop("insumos_df", None)

if conectar:
    try:
        df = query_insumos(host, port, service, sid, user, password, schema)
        st.session_state["insumos_df"] = df
        st.success(f"✅ {len(df)} registros carregados de `{schema}.INSUMOS`.")
    except ModuleNotFoundError:
        st.error("Pacote `oracledb` não está instalado neste ambiente. Instale com: `pip install oracledb`")
    except Exception as e:
        st.error("❌ Não foi possível conectar ou consultar o Oracle.")
        st.exception(e)

# Se já há dados na sessão, usa; assim o slider e filtros não resetam a página
df = st.session_state.get("insumos_df")

st.divider()
if df is None or df.empty:
    st.info("Clique em **Conectar e carregar do Oracle** para continuar.")
    st.stop()

# =========================
# KPIs rápidos
# =========================
total_reg = int(len(df))
total_insumos = int(df["INSUMO"].nunique()) if "INSUMO" in df else 0
qtd_total = int(df["QUANTIDADE"].sum()) if "QUANTIDADE" in df else 0
qtd_mediana = int(df["QUANTIDADE"].median()) if "QUANTIDADE" in df and len(df) > 0 else 0

k1, k2, k3, k4 = st.columns(4)
k1.metric("Registros", f"{total_reg:,}".replace(",", "."))
k2.metric("Itens únicos (INSUMO)", f"{total_insumos:,}".replace(",", "."))
k3.metric("Quantidade total", f"{qtd_total:,}".replace(",", "."))
k4.metric("Mediana de quantidade", f"{qtd_mediana:,}".replace(",", "."))

st.divider()

# =========================
# Filtros avançados
# =========================
st.subheader("Filtros e visão")
colF1, colF2, colF3 = st.columns([0.4, 0.3, 0.3])

with colF1:
    termo = st.text_input("🔍 Filtrar por nome do insumo (contém)", "")
with colF2:
    exames_unicos = ["(todos)"] + sorted(df["EXAME"].dropna().unique().tolist()) if "EXAME" in df else ["(todos)"]
    exame_sel = st.selectbox("Filtrar por exame", exames_unicos)
with colF3:
    if "QUANTIDADE" in df:
        qmin, qmax = int(df["QUANTIDADE"].min()), int(df["QUANTIDADE"].max())
    else:
        qmin, qmax = 0, 0
    faixa = st.slider("Faixa de quantidade", qmin, qmax, (qmin, qmax))

# Multiselect de insumos (útil em estoques grandes)
insumos_opts = sorted(df["INSUMO"].dropna().unique().tolist()) if "INSUMO" in df else []
insumos_sel = st.multiselect("Selecionar insumos específicos (opcional)", insumos_opts, default=[])

# Aplica filtros
df_view = df.copy()
if termo:
    df_view = df_view[df_view["INSUMO"].str.contains(termo, case=False, na=False)]
if exame_sel != "(todos)":
    df_view = df_view[df_view["EXAME"] == exame_sel]
if insumos_sel:
    df_view = df_view[df_view["INSUMO"].isin(insumos_sel)]
if "QUANTIDADE" in df_view:
    df_view = df_view[(df_view["QUANTIDADE"] >= faixa[0]) & (df_view["QUANTIDADE"] <= faixa[1])]

# =========================
# Preview e download
# =========================
st.subheader("Preview dos dados filtrados")
st.dataframe(df_view, use_container_width=True, height=320)

csv_bytes = df_view.to_csv(index=False).encode("utf-8")
st.download_button(
    "⬇️ Baixar CSV (dados filtrados)",
    data=csv_bytes,
    file_name="insumos_filtrados.csv",
    mime="text/csv",
    use_container_width=True
)

st.divider()

# =========================
# Gráficos — seleção e modos
# =========================
st.subheader("Visualizações")

# 1) Top-N por insumo (barra)
with st.container():
    st.markdown("### 📦 Top insumos por quantidade")
    top_n = st.slider("Quantos itens exibir", 3, 30, 10, key="topn")
    top_df = (
        df_view.groupby("INSUMO", as_index=False)["QUANTIDADE"]
               .sum()
               .sort_values("QUANTIDADE", ascending=False)
               .head(top_n)
    )
    if top_df.empty:
        st.warning("Nenhum dado após os filtros.")
    else:
        fig1 = px.bar(top_df, x="INSUMO", y="QUANTIDADE", text="QUANTIDADE", title="Top insumos")
        fig1.update_traces(textposition="outside")
        fig1.update_layout(margin=dict(l=10, r=10, t=40, b=10), height=380)
        st.plotly_chart(fig1, use_container_width=True)

# 2) Agregações flexíveis: escolha eixo e gráfico
st.markdown("### 🧭 Exploração por agregação")
colA, colB, colC = st.columns([0.4, 0.3, 0.3])
with colA:
    eixo = st.selectbox("Agrupar por", ["EXAME", "INSUMO"])
with colB:
    metrica = st.selectbox("Métrica", ["Soma", "Média", "Mediana", "Máximo", "Mínimo"])
with colC:
    tipo = st.selectbox("Gráfico", ["Barra", "Pizza", "Treemap"])

if df_view.empty:
    st.info("Ajuste os filtros acima para visualizar as agregações.")
else:
    agg_map = {
        "Soma": "sum",
        "Média": "mean",
        "Mediana": "median",
        "Máximo": "max",
        "Mínimo": "min",
    }
    agg_df = (
        df_view.groupby(eixo, as_index=False)["QUANTIDADE"]
               .agg(agg_map[metrica])
               .rename(columns={"QUANTIDADE": metrica})
               .sort_values(metrica, ascending=(metrica=="Mínimo"))
    )

    if tipo == "Barra":
        fig = px.bar(agg_df, x=eixo, y=metrica, title=f"{metrica} de QUANTIDADE por {eixo}")
    elif tipo == "Pizza":
        fig = px.pie(agg_df, names=eixo, values=metrica, title=f"{metrica} por {eixo}")
    else:  # Treemap
        fig = px.treemap(agg_df, path=[eixo], values=metrica, title=f"{metrica} por {eixo}")

    fig.update_layout(margin=dict(l=10, r=10, t=40, b=10), height=420)
    st.plotly_chart(fig, use_container_width=True)

# 3) Comparar exames (stacked bar)
st.markdown("### 🧪 Comparar exames (barras empilhadas)")
exames_comp = st.multiselect("Escolha exames para comparar", sorted(df["EXAME"].dropna().unique().tolist()))
if exames_comp:
    df_comp = df_view[df_view["EXAME"].isin(exames_comp)]
    if df_comp.empty:
        st.warning("Nenhum dado após os filtros/seleção.")
    else:
        # agrega por insumo e exame
        pivot = (df_comp.groupby(["INSUMO", "EXAME"], as_index=False)["QUANTIDADE"].sum())
        fig3 = px.bar(pivot, x="INSUMO", y="QUANTIDADE", color="EXAME", barmode="stack",
                      title="Quantidade por Insumo (exames selecionados)")
        fig3.update_layout(margin=dict(l=10, r=10, t=40, b=10), height=420)
        st.plotly_chart(fig3, use_container_width=True)

st.caption("Use **Atualizar** após inserir novos registros no Oracle para recarregar.")
