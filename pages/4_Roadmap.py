# pages/4_Roadmap.py
# -*- coding: utf-8 -*-

import streamlit as st
import json
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

# ========= Config =========
st.set_page_config(
    page_title="Roadmap | Estoque Inteligente (QR → ML)",
    page_icon="🛣️",
    layout="wide",
)

st.title("🛣️ Roadmap da Solução")
st.caption("Evolução planejada em fases — do QR até Machine Learning")

st.markdown("""
O roadmap abaixo mostra como a solução pode ser **implementada de forma incremental**,  
trazendo resultados **rápidos** já no curto prazo e abrindo espaço para **inovações avançadas** no futuro.
""")

# ========= Timeline =========
try:
    from streamlit_timeline import timeline

    roadmap = {
        "title": {
            "text": {
                "headline": "Roadmap da Solução",
                "text": "Evolução incremental do QR → ML"
            }
        },
        "events": [
            {
                "start_date": {"year": 2025},
                "text": {
                    "headline": "📷 Fase 1 — Curto prazo",
                    "text": "Leitura QR/Barcode via câmera<br>Registro automático entrada/saída<br>Painel local em tempo real"
                },
                "media": {
                    "url": "https://cdn-icons-png.flaticon.com/512/2972/2972185.png",
                    "caption": "Fase 1: Automação com QR/Barcode"
                }
            },
            {
                "start_date": {"year": 2026},
                "text": {
                    "headline": "🤖 Fase 2 — Médio prazo",
                    "text": "Machine Learning para reconhecer insumos pela embalagem<br>Menos dependência de QR<br>Mais automação, menos erro humano"
                },
                "media": {
                    "url": "https://cdn-icons-png.flaticon.com/512/4712/4712109.png",
                    "caption": "Fase 2: Machine Learning detectando insumos"
                }
            },
            {
                "start_date": {"year": 2027},
                "text": {
                    "headline": "🔗 Fase 3 — Médio/Longo prazo",
                    "text": "Integração com SAP/ERP DASA<br>Atualização em tempo real<br>Alertas automáticos de reposição e validade"
                },
                "media": {
                    "url": "https://cdn-icons-png.flaticon.com/512/3209/3209265.png",
                    "caption": "Fase 3: Integração SAP/ERP"
                }
            },
            {
                "start_date": {"year": 2028},
                "text": {
                    "headline": "📊 Fase 4 — Longo prazo",
                    "text": "Dashboards avançados<br>IA preditiva para prever rupturas<br>Otimização de compras e custos"
                },
                "media": {
                    "url": "https://cdn-icons-png.flaticon.com/512/1828/1828884.png",
                    "caption": "Fase 4: Dashboards inteligentes com IA preditiva"
                }
            }
        ]
    }

    timeline(json.dumps(roadmap), height=600)

except:
    st.warning("⚠️ Para visualizar a linha do tempo interativa, instale `streamlit-timeline`:\n```bash\npip install streamlit-timeline\n```")

    # Fallback simples
    fases = [
        ("📷 Fase 1 — Curto prazo", "- QR/Barcode + painel local em tempo real"),
        ("🤖 Fase 2 — Médio prazo", "- Machine Learning para reconhecimento por imagem"),
        ("🔗 Fase 3 — Médio/Longo prazo", "- Integração SAP/ERP + alertas automáticos"),
        ("📊 Fase 4 — Longo prazo", "- IA preditiva + dashboards avançados"),
    ]
    for titulo, desc in fases:
        st.subheader(titulo)
        st.markdown(desc)
        st.divider()

# ========= Conclusão =========
st.success("✅ Este roadmap mostra que a solução começa simples (QR), já gera valor imediato e evolui até IA preditiva para uma gestão de estoque totalmente automatizada.")
