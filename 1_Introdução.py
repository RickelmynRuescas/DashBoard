# pages/1_Introdução.py
# -*- coding: utf-8 -*-

import os
import time
import pandas as pd
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

# ======= (Opcional) Lottie para dar vida =======
try:
    from streamlit_lottie import st_lottie
    _HAS_LOTTIE = True
except Exception:
    _HAS_LOTTIE = False

# ----------------- Config -----------------
st.set_page_config(
    page_title="Introdução | Estoque Inteligente (QR → ML)",
    page_icon="📦",
    layout="wide",
)

# ----------------- Header -----------------
colA, colB = st.columns([0.75, 0.25])
with colA:
    st.title("📦 StockFlow - Estoque Inteligente em Tempo Real (QR → ML)")
    st.caption("Automação do apontamento de consumo de insumos via câmera — DASA")

    # ----------------- Infográfico do Pipeline (N O V O) -----------------
st.divider()
st.subheader("🔎 Pipeline de Captura → Detecção → Reconhecimento → Informação em Tempo Real")

# tente primeiro a imagem corrigida; se não existir, usa um fallback
candidate_paths = [
    "images/scan.png",   # coloque aqui a imagem corrigida
    
]
pipeline_img = next((p for p in candidate_paths if os.path.exists(p)), None)

IMG_WIDTH = st.slider("Largura da imagem (px)", 380, 900, 700 , 10)
st.image(pipeline_img, width=IMG_WIDTH)


with st.expander("O que este pipeline entrega na prática?"):
    st.markdown("""
- **(1) Visualização:** câmera cobre a área de prateleiras do almoxarifado/sala.  
- **(2) Detecção/Identificação:** o sistema destaca regiões de interesse e extrai **cor, textura e proporção**.  
- **(3) Reconhecimento:** compara características e confirma o item (ex.: soro, seringa).  
- **(4) Informação em Tempo Real:** atualiza **estoque**, sinaliza **mínimos** e **validade**, e registra a **baixa/entrada**.
""")


# ----------------- Objetivo -----------------
st.subheader("Objetivo")
st.write(
    "Dar **visibilidade em tempo real** ao consumo de insumos e **automatizar** entradas/saídas, "
    "reduzindo o erro humano e suportando decisões de **reposição** e **validade**."
)

# ----------------- Abas: Ideia Central -----------------
tab_qr, tab_ml = st.tabs(["🟩 Fase 1 — QR/Barcode (agora)", "🟦 Fase 2 — Machine Learning (futuro)"])

with tab_qr:
    st.markdown("""
**Como funciona (MVP):**  
A câmera lê o **QR/código de barras** do insumo ao passar por uma área de leitura → o sistema registra **baixa/entrada automática** → o painel mostra **estoque atual**, **alertas de mínimo** e **validade**.

**Por que começar por aqui?**  
- Baixo custo e alta viabilidade.  
- Reduz digitação e erros imediatamente.  
- Serve como fallback mesmo quando houver ML.
    """)
    pros, cons = st.columns(2)
    with pros:
        st.success("**Prós:** simples, barato, confiável; ganho rápido de produtividade.")
    with cons:
        st.warning("**Atenção:** precisa de etiqueta no insumo; ainda não reconhece por imagem.")

with tab_ml:
    st.markdown("""
**Como funciona (evolução):**  
Usamos **visão computacional** para **classificar/detectar** o insumo pela imagem (embalagem, formato, rótulo), "
"sem necessidade de etiqueta. Com **tracking + linha virtual**, registramos **entrada × saída** automaticamente.

**Por que evoluir?**  
- Remove dependência de etiqueta.  
- Reconhece múltiplos itens na cena, com contagem.
    """)
    pros2, cons2 = st.columns(2)
    with pros2:
        st.success("**Prós:** elimina etiquetas; visão mais autônoma e fluida.")
    with cons2:
        st.warning("**Atenção:** precisa de **dataset**, validação e, às vezes, GPU. Maior complexidade.")

# ----------------- KPIs (mock) -----------------
st.divider()
st.subheader("📊 Visão rápida (mock de KPIs)")

# Parâmetros de simulação
col1, col2, col3, col4 = st.columns(4)
with col1:
    eventos_mes = st.number_input("Eventos/mês (saídas/entradas)", 100, 100000, 5000, step=100)
with col2:
    # CORREÇÃO: slider em porcentagem inteira 0–20 e conversão para fração
    erro_manual_pct = st.slider("Erro manual atual (estimado)", 0, 20, 8, 1, format="%d%%")
    erro_manual = erro_manual_pct / 100.0
with col3:
    adocao_qr = st.slider("Adoção QR/Barcode (fase 1)", 0, 100, 70, 5, format="%d%%")
with col4:
    adocao_ml = st.slider("Adoção ML (fase 2)", 0, 100, 0, 5, format="%d%%")

# Cálculo simples
erros_atuais = int(eventos_mes * erro_manual)
redu_qr = int(erros_atuais * (adocao_qr/100) * 0.75)   # suposição: QR reduz 75% dos erros nas áreas cobertas
redu_ml = int(erros_atuais * (adocao_ml/100) * 0.90)   # suposição: ML reduz 90% dos erros nas áreas cobertas
erros_proj = max(erros_atuais - redu_qr - redu_ml, 0)

m1, m2, m3 = st.columns(3)
m1.metric("Erros/mês (estimado - hoje)", f"{erros_atuais:,}".replace(",", "."))
m2.metric("Erros/mês (projeção com QR→ML)", f"{erros_proj:,}".replace(",", "."), delta=f"-{(erros_atuais-erros_proj):,}".replace(",", "."))
m3.metric("Automação prevista", f"{adocao_qr + adocao_ml}%")

# Gráfico
df_plot = pd.DataFrame({
    "Cenário": ["Hoje (manual)", "Com QR", "Com QR + ML"],
    "Erros": [erros_atuais, max(erros_atuais - redu_qr, 0), erros_proj],
})
st.bar_chart(df_plot, x="Cenário", y="Erros", use_container_width=True)

# ----------------- Mini “replay” do pipeline -----------------
st.divider()
st.subheader("🧪 Mini replay do pipeline (QR → ML)")

colL, colR = st.columns([0.55, 0.45])
with colL:
    modo = st.radio("Selecione o modo para visualizar o fluxo:", ["QR/Barcode", "Machine Learning"], horizontal=True)
    if st.button("▶️ Executar replay"):
        with st.spinner("Iniciando captura de câmera..."):
            time.sleep(0.6)
        st.toast("🎥 Câmera conectada", icon="✅")
        time.sleep(0.4)
        if modo == "QR/Barcode":
            st.info("🔍 Lendo código QR/Barcode...", icon="🔎")
            time.sleep(0.8)
            st.success("✅ Código identificado: INS-002 (Swab estéril)")
            time.sleep(0.6)
            st.info("📦 Ação: **BAIXA** no estoque (1 unidade)")
            time.sleep(0.5)
            st.success("💾 Evento registrado (timestamp, SKU, ação)")
        else:
            st.info("🧠 Rodando modelo de classificação/detecção...", icon="🧠")
            time.sleep(0.8)
            st.success("✅ Classe detectada: **Seringa 5ml** (conf. 0.94)")
            time.sleep(0.6)
            st.info("↔️ Tracking + linha virtual: direção detectada → **SAÍDA**")
            time.sleep(0.6)
            st.success("💾 Evento registrado (timestamp, classe, confiança, ação)")

with colR:
    st.markdown("**Fluxo esperado:**")
    steps = [
        "1) Captura de imagem (câmera IP/USB)", 
        "2) Reconhecimento (QR) ou Classificação/Detecção (ML)",    
        "3) Regras de negócio (baixa/entrada, mínimos, validade)",
        "4) Persistência (log/DB) e atualização de painel",
        "5) KPIs e alertas em tempo real",
    ]
    for s in steps:
        st.write("• " + s)

# ----------------- Navegação -----------------
st.info("Esta página apresenta a **introdução**. As próximas páginas aprofundam solução, protótipos e métricas.")

