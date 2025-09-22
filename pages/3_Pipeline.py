# pages/3_Pipeline.py
# -*- coding: utf-8 -*-

import streamlit as st
import time
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
    page_title="Pipeline da Solução | Estoque Inteligente (QR → ML)",
    page_icon="🔄",
    layout="wide",
)

# ----------------- Header -----------------
st.title("🔄 Pipeline da Solução — QR → ML")
st.caption("Fluxo interativo do processo de automação do estoque")

st.markdown("""
Aqui mostramos o **passo a passo** do fluxo da solução, do momento em que o insumo passa pela câmera até aparecer no painel do almoxarifado.
""")

# ----------------- Cards de explicação -----------------
st.subheader("📍 Etapas do Pipeline")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("### 1️⃣ Captura da imagem")
    st.info("Câmera capta a passagem do insumo (entrada ou saída).")

    st.markdown("### 2️⃣ Reconhecimento")
    st.info("Leitura de **QR/Barcode** (fase inicial) ou **Machine Learning** (futuro).")

with col2:
    st.markdown("### 3️⃣ Regras de negócio")
    st.info("Define se foi **entrada** ou **baixa**, valida quantidade mínima e validade.")

    st.markdown("### 4️⃣ Atualização")
    st.info("Estoque atualizado automaticamente em tempo real.")

with col3:
    st.markdown("### 5️⃣ Painel")
    st.info("Interface mostra saldos, alertas de ruptura e validade.")

st.divider()

# ----------------- Inserindo a imagem -----------------
st.subheader("📸 Exemplo ilustrativo do pipeline em ação")
st.image(
    "images/camera_qr.png",
    caption="Câmera captando insumo com QR Code no almoxarifado",
    width=700  # 🔽 ajusta a largura da imagem
)


# ----------------- Simulação Interativa -----------------
st.subheader("▶️ Simulação do Pipeline")

if st.button("Executar pipeline passo a passo"):
    with st.spinner("1️⃣ Capturando imagem..."):
        time.sleep(1.2)
    st.success("✅ Imagem capturada pela câmera.")

    with st.spinner("2️⃣ Reconhecendo insumo..."):
        time.sleep(1.2)
    st.success("✅ Insumo identificado: *Seringa 5ml* (via QR).")

    with st.spinner("3️⃣ Aplicando regras de negócio..."):
        time.sleep(1.2)
    st.success("✅ Baixa registrada (1 unidade).")

    with st.spinner("4️⃣ Atualizando estoque..."):
        time.sleep(1.2)
    st.success("✅ Estoque atualizado: 99 unidades restantes.")

    with st.spinner("5️⃣ Exibindo no painel..."):
        time.sleep(1.2)
    st.success("✅ Painel atualizado com alerta: Estoque próximo do mínimo.")

st.info("Essa simulação demonstra como o fluxo automatizado elimina erros e atualiza o sistema em tempo real.")

# ----------------- Navegação -----------------
st.divider()
