# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
from datetime import datetime
from config import SMARTSHEET_TOKEN, SMARTSHEET_SHEET_ID
from modules.smartsheet_api import SmartsheetManager
from modules.ibge_api import IBGEService
from modules.charts import HighchartsRenderer

st.set_page_config(
    page_title="Pesquisa de Satisfacao - Facilities",
    page_icon="\U0001f4cb",
    layout="wide",
)

st.markdown(
    """
<div style="text-align:center; padding:20px; background:linear-gradient(135deg,#1a1a2e,#0f3460);
     color:white; border-radius:12px; margin-bottom:25px;">
    <h1>&#128203; Pesquisa de Satisfa&#231;&#227;o</h1>
    <h3>Servi&#231;os de Facilities | 1&#186; Semestre 2026</h3>
    <p>Avalie sua satisfa&#231;&#227;o com transporte, portaria, vigil&#226;ncia, limpeza, jardinagem e refei&#231;&#227;o</p>
    <span style="background:#28a745; padding:5px 15px; border-radius:20px; font-size:0.85em;">
        &#128274; 100% An&#244;nimo
    </span>
</div>
""",
    unsafe_allow_html=True,
)

smartsheet = SmartsheetManager()
ibge = IBGEService()
charts = HighchartsRenderer()

ESCALA = {
    1: "1 - Muito insatisfeito",
    2: "2 - Insatisfeito",
    3: "3 - Neutro",
    4: "4 - Satisfeito",
    5: "5 - Muito satisfeito",
}

SERVICOS = ["Transporte", "Portaria", "Vigilancia", "Limpeza", "Jardinagem", "Refeicao"]

tab_avaliar, tab_resultados = st.tabs(["Avaliar", "Resultados"])

with tab_avaliar:
    if "ja_respondeu" not in st.session_state:
        st.session_state.ja_respondeu = False

    if st.session_state.ja_respondeu:
        st.success("Voce ja enviou sua avaliacao. Obrigado pela participacao!")
        st.info("Cada pessoa pode responder apenas uma vez.")
    else:
        st.markdown("""
        **Prezado(a) colaborador(a),**

        Sua opiniao e essencial para a melhoria continua dos nossos servicos de Facilities.
        Por favor, avalie os aspectos abaixo utilizando a seguinte escala:

        1 - Muito insatisfeito | 2 - Insatisfeito | 3 - Neutro | 4 - Satisfeito | 5 - Muito satisfeito
        """)

        st.divider()

        with st.form("form_avaliacao", clear_on_submit=True):

            st.markdown("### 1. Transporte")
            transporte_nota = st.radio(
                "Qual sua satisfacao com o servico de transporte?",
                options=[1, 2, 3, 4, 5],
                index=None,
                format_func=lambda x: ESCALA[x],
                horizontal=True,
                key="transporte_nota",
            )
            transporte_comentario = st.text_input(
                "Compartilhe seus comentarios ou sugestoes sobre o transporte:",
                key="transporte_com",
            )

            st.divider()

            st.markdown("### 2. Portaria")
            portaria_nota = st.radio(
                "Qual sua satisfacao com o servico de portaria?",
                options=[1, 2, 3, 4, 5],
                index=None,
                format_func=lambda x: ESCALA[x],
                horizontal=True,
                key="portaria_nota",
            )
            portaria_comentario = st.text_input(
                "Compartilhe sua opiniao sobre a portaria:",
                key="portaria_com",
            )

            st.divider()

            st.markdown("### 3. Vigilancia")
            vigilancia_nota = st.radio(
                "Qual sua satisfacao com o servico de vigilancia?",
                options=[1, 2, 3, 4, 5],
                index=None,
                format_func=lambda x: ESCALA[x],
                horizontal=True,
                key="vigilancia_nota",
            )
            vigilancia_comentario = st.text_input(
                "Compartilhe sua opiniao sobre a vigilancia:",
                key="vigilancia_com",
            )

            st.divider()

            st.markdown("### 4. Limpeza")
            limpeza_nota = st.radio(
                "Qual sua satisfacao com o servico de limpeza?",
                options=[1, 2, 3, 4, 5],
                index=None,
                format_func=lambda x: ESCALA[x],
                horizontal=True,
                key="limpeza_nota",
            )
            limpeza_comentario = st.text_input(
                "Compartilhe sua opiniao sobre a limpeza:",
                key="limpeza_com",
            )

            st.divider()

            st.markdown("### 5. Jardinagem")
            jardinagem_nota = st.radio(
                "Qual sua satisfacao com o servico de jardinagem?",
                options=[1, 2, 3, 4, 5],
                index=None,
                format_func=lambda x: ESCALA[x],
                horizontal=True,
                key="jardinagem_nota",
            )
            jardinagem_comentario = st.text_input(
                "Compartilhe sua opiniao sobre a jardinagem:",
                key="jardinagem_com",
            )

            st.divider()

            st.markdown("### 6. Refeicao")
            refeicao_nota = st.radio(
                "Qual sua satisfacao com o servico de refeicao?",
                options=[1, 2, 3, 4, 5],
                index=None,
                format_func=lambda x: ESCALA[x],
                horizontal=True,
                key="refeicao_nota",
            )
            refeicao_comentario = st.text_input(
                "Compartilhe sua opiniao sobre as refeicoes:",
                key="refeicao_com",
            )

            st.divider()

            st.markdown("### 7. Satisfacao Geral (NPS)")
            nps = st.radio(
                "Em uma escala de 0 a 10, qual e sua satisfacao geral com os servicos de Facilities?",
                options=list(range(0, 11)),
                index=None,
                horizontal=True,
                key="nps_nota",
            )

            st.divider()

            st.markdown("### 8. Qual servico precisa de mais atencao?")
            servico_atencao = st.multiselect(
                "Selecione um ou mais:",
                options=SERVICOS,
                key="servico_atencao",
            )

            st.divider()

            st.markdown("### 9. Percebeu melhoria nos ultimos 6 meses?")
            percebeu_melhoria = st.radio(
                "Voce percebeu alguma melhoria nos servicos de Facilities?",
                options=["Sim", "Nao", "Nao tenho certeza"],
                index=None,
                horizontal=True,
                key="melhoria",
            )

            st.divider()

            st.markdown("### 10. Sugestoes")
            sugestoes = st.text_area(
                "Deixe suas ideias ou sugestoes para aprimorar os servicos:",
                max_chars=1000,
                key="sugestoes",
            )

            st.divider()

            st.markdown("### Localizacao")
            col1, col2 = st.columns(2)

            with col1:
                estados = ibge.listar_estados()
                estado_options = {e["nome"]: e["id"] for e in estados}
                estado = st.selectbox("Estado:", [""] + list(estado_options.keys()))

            with col2:
                municipio = ""
                if estado:
                    municipios = ibge.listar_municipios(estado_options[estado])
                    mun_nomes = [m["nome"] for m in municipios]
                    municipio = st.selectbox("Municipio:", [""] + mun_nomes)
                else:
                    st.selectbox("Municipio:", ["Selecione o estado primeiro"])

            st.divider()

            submitted = st.form_submit_button(
                "Enviar Avaliacao", use_container_width=True, type="primary"
            )

            if submitted:
                if not estado:
                    st.error("Selecione seu estado.")
                else:
                    dados = {
                        "transporte_nota": transporte_nota,
                        "transporte_comentario": transporte_comentario,
                        "portaria_nota": portaria_nota,
                        "portaria_comentario": portaria_comentario,
                        "vigilancia_nota": vigilancia_nota,
                        "vigilancia_comentario": vigilancia_comentario,
                        "limpeza_nota": limpeza_nota,
                        "limpeza_comentario": limpeza_comentario,
                        "jardinagem_nota": jardinagem_nota,
                        "jardinagem_comentario": jardinagem_comentario,
                        "refeicao_nota": refeicao_nota,
                        "refeicao_comentario": refeicao_comentario,
                        "nps": nps,
                        "servico_atencao": ", ".join(servico_atencao) if servico_atencao else "",
                        "percebeu_melhoria": percebeu_melhoria,
                        "sugestoes": sugestoes,
                        "estado": estado,
                        "municipio": municipio,
                        "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    }
                    if smartsheet.enviar_avaliacao(dados):
                        st.session_state.ja_respondeu = True
                        st.success("Avaliacao enviada com sucesso!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("Erro ao enviar. Tente novamente.")

with tab_resultados:
    st.subheader("Dashboard de Resultados")

    df = smartsheet.buscar_avaliacoes()

    if df.empty:
        st.info("Nenhuma avaliacao registrada ainda.")
    else:
        notas_cols = [
            "transporte_nota", "portaria_nota", "vigilancia_nota",
            "limpeza_nota", "jardinagem_nota", "refeicao_nota"
        ]
        notas_labels = ["Transporte", "Portaria", "Vigilancia", "Limpeza", "Jardinagem", "Refeicao"]

        for col in notas_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        if "nps" in df.columns:
            df["nps"] = pd.to_numeric(df["nps"], errors="coerce")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Respostas", len(df))
        with col2:
            media_geral = df[notas_cols].mean().mean()
            st.metric("Media Geral", f"{media_geral:.1f}/5")
        with col3:
            if "nps" in df.columns:
                nps_medio = df["nps"].mean()
                st.metric("NPS Medio", f"{nps_medio:.1f}/10")
        with col4:
            melhor_idx = df[notas_cols].mean().idxmax()
            melhor_servico = notas_labels[notas_cols.index(melhor_idx)]
            st.metric("Melhor Avaliado", melhor_servico)

        st.divider()

        medias = [round(df[col].mean(), 2) for col in notas_cols]

        config_radar = {
            "chart": {"polar": True, "type": "line"},
            "title": {"text": "Satisfacao por Servico"},
            "pane": {"size": "85%"},
            "xAxis": {"categories": notas_labels, "tickmarkPlacement": "on"},
            "yAxis": {"gridLineInterpolation": "polygon", "min": 0, "max": 5},
            "series": [{"name": "Media", "data": medias, "pointPlacement": "on"}],
        }
        charts.render_chart(config_radar, height=500)

        ranking_data = sorted(zip(notas_labels, medias), key=lambda x: x[1], reverse=True)
        charts.ranking_barras(
            [r[0] for r in ranking_data],
            [r[1] for r in ranking_data]
        )

        if "nps" in df.columns:
            st.markdown("### Net Promoter Score (NPS)")
            promotores = len(df[df["nps"] >= 9])
            neutros = len(df[(df["nps"] >= 7) & (df["nps"] <= 8)])
            detratores = len(df[df["nps"] <= 6])
            total = len(df)
            nps_score = ((promotores - detratores) / total) * 100

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Promotores (9-10)", promotores)
            with col2:
                st.metric("Neutros (7-8)", neutros)
            with col3:
                st.metric("Detratores (0-6)", detratores)
            with col4:
                st.metric("NPS Score", f"{nps_score:.0f}")

        if "servico_atencao" in df.columns:
            st.markdown("### Servico que Precisa de Mais Atencao")
            atencao_list = df["servico_atencao"].dropna().str.split(", ").explode()
            if not atencao_list.empty:
                contagem = atencao_list.value_counts()
                config_atencao = {
                    "chart": {"type": "bar"},
                    "title": {"text": "Servicos que Precisam de Mais Atencao"},
                    "xAxis": {"categories": contagem.index.tolist()},
                    "yAxis": {"title": {"text": "Votos"}},
                    "series": [{"name": "Respostas", "data": [int(v) for v in contagem.values], "showInLegend": False}],
                    "plotOptions": {"bar": {"borderRadius": 5, "dataLabels": {"enabled": True}}},
                }
                charts.render_chart(config_atencao)

        if "percebeu_melhoria" in df.columns:
            st.markdown("### Percebeu Melhoria nos Ultimos 6 Meses?")
            melhoria_count = df["percebeu_melhoria"].value_counts()
            config_melhoria = {
                "chart": {"type": "pie"},
                "title": {"text": "Percepcao de Melhoria"},
                "plotOptions": {"pie": {"innerSize": "50%", "dataLabels": {"enabled": True, "format": "{point.name}: {point.percentage:.1f}%"}}},
                "series": [{"name": "Respostas", "data": [
                    {"name": str(nome), "y": int(qtd)} for nome, qtd in melhoria_count.items()
                ]}],
            }
            charts.render_chart(config_melhoria)