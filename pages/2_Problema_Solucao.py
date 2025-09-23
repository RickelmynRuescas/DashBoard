# pages/2_Problema_Solucao.py
# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
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

# ----------------- Config -----------------
st.set_page_config(
    page_title="Problema & Solução Detalhados | Estoque Inteligente (QR → ML)",
    page_icon="📊",
    layout="wide",
)

# ----------------- Header -----------------
st.title("📊 Problema & Solução — Aprofundamento")
st.caption("Foco em divergências reais (SAP × estoque físico), causas e como o fluxo automatizado resolve")

# ============================================================
# 1) Auditoria de divergências (apenas resultado)
# ============================================================
st.subheader("1) Auditoria rápida de divergências (SAP × Real)")
st.markdown("Abaixo, o **resultado** da auditoria com deltas e itens críticos.")

# Base fixa (sem editor)
dados_base = pd.DataFrame({
    "Insumo": ["Seringa 5ml", "Swab estéril", "Tubo EDTA 4ml", "Luva nitrílica G", "Tubo Citrato 3,2%"],
    "Estoque SAP": [120, 85, 200, 150, 60],
    "Estoque Real": [100, 60, 240, 110, 70],
    "Mínimo Operacional": [80, 50, 150, 120, 50],
})

# Apenas a tabela de RESULTADO (sem a primeira tabela editável)
df = dados_base.copy()
df["Delta (Real - SAP)"] = df["Estoque Real"] - df["Estoque SAP"]
df["Abaixo do Mínimo?"] = np.where(df["Estoque Real"] < df["Mínimo Operacional"], "⚠️ Sim", "OK")

st.markdown("**Resultado da auditoria:**")
st.dataframe(df, use_container_width=True)

# Gráfico de barras: SAP vs Real
fig = px.bar(
    df.melt(id_vars=["Insumo"], value_vars=["Estoque SAP", "Estoque Real"],
            var_name="Origem", value_name="Quantidade"),
    x="Insumo", y="Quantidade", color="Origem", barmode="group",
    title="Comparativo de Estoque: SAP × Real"
)
st.plotly_chart(fig, use_container_width=True)

# ============================================================
# 2) Como o processo funciona: Hoje vs Automatizado (QR → ML)
# ============================================================
st.subheader("2) Processo: Hoje × Automatizado (QR → ML)")

col_hj, col_auto = st.columns(2)
with col_hj:
    st.markdown("### Hoje (manual)")
    st.error(
        "- Técnico retira insumo e **não registra** na hora\n"
        "- Encarregado **atualiza depois** no SAP, quando possível\n"
        "- **Atraso** e **erros de digitação** acumulam\n"
        "- Estoque em sistema **não bate** com o físico"
    )

with col_auto:
    st.markdown("### Com automação (QR → ML)")
    st.success(
        "- **QR** (agora) ou **ML** (futuro) identifica automaticamente o insumo\n"
        "- **Baixa/entrada em tempo real** no momento do evento\n"
        "- Painel **atualiza saldo** e **alertas** (mínimo, validade)\n"
        "- Estoque em sistema **espelha a realidade**"
    )

st.info("Conclusão: a automação **ataca a raiz** da divergência — o **atraso e erro humano** no apontamento.")

# ============================================================
# 3) Causa → Efeito e Mitigação
# ============================================================
st.subheader("3) Causa → Efeito e Mitigação")

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("#### Causas")
    st.markdown(
        "- Apontamento manual e tardio\n"
        "- Operador com múltiplas tarefas\n"
        "- Falta de confirmação no ato do consumo\n"
        "- Sem visibilidade do mínimo/validade"
    )

with c2:
    st.markdown("#### Efeitos")
    st.markdown(
        "- Divergência SAP × Real\n"
        "- **Ruptura** de insumos críticos\n"
        "- **Excesso** parado e capital imobilizado\n"
        "- Retrabalho e auditorias frequentes"
    )

with c3:
    st.markdown("#### Mitigação (QR → ML)")
    st.markdown(
        "- Captura automática no **momento do evento**\n"
        "- **Logs** e rastreabilidade por timestamp\n"
        "- **Alertas** de mínimo e validade (FEFO)\n"
        "- Base confiável p/ decisão e compra"
    )

# ============================================================
# 4) Critérios de sucesso
# ============================================================
st.subheader("4) Critérios de sucesso (definição clara)")
st.markdown(
    "- **Divergência SAP × Real** ↓ (meta: ~0 no piloto)\n"
    "- **% de eventos automatizados** ↑ (QR no início; ML nas classes cobertas)\n"
    "- **Tempo de atualização** → próximo de **tempo real**\n"
    "- **Incidentes de ruptura** ↓ e **perdas por validade** ↓"
)

st.divider()
st.caption("Esta página aprofunda a dor com dados, explica o porquê das divergências e mostra como o fluxo QR → ML resolve a raiz do problema — sem repetir a Introdução.")
