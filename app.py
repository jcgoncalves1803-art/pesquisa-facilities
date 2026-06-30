# -*- codificação: utf-8 -*-
importar streamlit como st
import pandas as pd
from datetime import datetime
from config import SMARTSHEET_TOKEN, SMARTSHEET_SHEET_ID
from modules.smartsheet_api import SmartsheetManager
from modules.ibge_api import IBGEService
from modules.charts import HighchartsRenderer

st.set_page_config(
    page_title="Pesquisa de Satisfação - Instalações",
    page_icon="ðŸ“‹",
    layout="amplo",
)

st.markdown(
    """
<div style="text-align:center; padding:20px; background:linear-gradient(135deg,#1a1a2e,#0f3460);
     cor:branca; raio da borda:12px; margem inferior:25px;">
    <h1>ðŸ“‹ Pesquisa de Satisfação</h1>
    <h3>Serviços de Facilities | 1º Semestre 2026</h3>
    <p>Avalie sua satisfação com transporte, portaria, vigilância, limpeza, jardinagem e refeição</p>
    <span style="background:#28a745; padding:5px 15px; border-radius:20px; font-size:0.85em;">
        ðŸ”' 100% Anônimo
    </span>
</div>
"",
    unsafe_allow_html=True,
)

smartsheet = SmartsheetManager()
ibge = IBGEService()
gráficos = HighchartsRenderer()

ESCALA = {
    1: "1 - Muito insatisfeito",
    2: "2 - Insatisfeito",
    3: "3 - Neutro",
    4: "4 - Satisfeito",
    5: "5 - Muito satisfeito",
}

SERVICOS = ["Transporte", "Portaria", "Vigilancia", "Limpeza", "Jardinagem", "Refeicao"]

tab_avaliar, tab_resultados = st.tabs(["ðŸ“ Avaliar", "ðŸ“Š Resultados"])

com tab_avaliar:
    se "ja_respondeu" não estiver em st.session_state:
        st.session_state.ja_respondeu = Falso

    se st.session_state.ja_respondeu:
        st.success("âœ… Você já está com inveja de sua avaliação. Obrigado pela participação!")
        st.info("Cada pessoa pode responder apenas uma vez.")
    outro:
        st.markdown("""
        **Prezado(a) colaborador(a),**

        Sua opinião é essencial para a melhoria contínua de nossos serviços de Facilities.
        Por favor, avalie os aspectos abaixo utilizando a seguinte escala:

        âœ… 1 - Muito insatisfeito | 2 - Insatisfeito | 3 - Neutro | 4 - Satisfeito | 5 - Muito satisfeito
        "")

        st.divider()

        com st.form("form_avaliacao", clear_on_submit=True):

            st.markdown("### ðŸšŒ 1. Transporte")
            transporte_nota = st.radio(
                "Qual sua satisfação com o serviço de transporte?",
                opções=[1, 2, 3, 4, 5],
                índice=Nenhum,
                formato_func=lambda x: ESCALA[x],
                horizontal=Verdadeiro,
                chave="transporte_nota",
            )
            transporte_comentário = st.text_input(
                "Compartilhe seus comentários ou sugestões sobre o transporte:",
                chave="transporte_com",
            )

            st.divider()

            st.markdown("### ðŸšª 2. Portaria")
            portaria_nota = st.radio(
                "Qual sua satisfação com o serviço de portaria?",
                opções=[1, 2, 3, 4, 5],
                índice=Nenhum,
                formato_func=lambda x: ESCALA[x],
                horizontal=Verdadeiro,
                chave="portaria_nota",
            )
            portaria_comentario = st.text_input(
                "Compartilhe sua opinião sobre a portaria:",
                chave="portaria_com",
            )

            st.divider()

            st.markdown("### ðŸ›¡ï¸ 3. Vigilância")
            vigilância_nota = st.radio(
                "Qual sua satisfação com o serviço de vigilância?",
                opções=[1, 2, 3, 4, 5],
                índice=Nenhum,
                formato_func=lambda x: ESCALA[x],
                horizontal=Verdadeiro,
                chave="vigilância_nota",
            )
            vigilante_comentario = st.text_input(
                "Compartilhe sua opinião sobre a vigilância:",
                chave="vigilância_com",
            )

            st.divider()

            st.markdown("### ðŸ§¹ 4. Limpeza")
            …_nota = st.radio(
                "Qual sua satisfação com o serviço de limpeza?",
                opções=[1, 2, 3, 4, 5],
                índice=Nenhum,
                formato_func=lambda x: ESCALA[x],
                horizontal=Verdadeiro,
                chave="limpeza_nota",
            )
            limpeza_comentário = st.text_input(
                "Compartilhe sua opinião sobre a limpeza:",
                chave="limpeza_com",
            )

            st.divider()

            st.markdown("### ðŸŒ¿ 5. Jardinagem")
            cultivar_nota = st.radio(
                "Qual sua satisfação com o serviço de jardinagem?",
                opções=[1, 2, 3, 4, 5],
                índice=Nenhum,
                formato_func=lambda x: ESCALA[x],
                horizontal=Verdadeiro,
                chave="jardinagem_nota",
            )
            jardinagem_comentário = st.text_input(
                "Compartilhe sua opinião sobre a jardinagem:",
                chave="jardinagem_com",
            )

            st.divider()

            st.markdown("### ðŸ ½ï¸ 6. Refeição")
            refeicao_nota = st.radio(
                "Qual sua satisfação com o serviço de refeição?",
                opções=[1, 2, 3, 4, 5],
                índice=Nenhum,
                formato_func=lambda x: ESCALA[x],
                horizontal=Verdadeiro,
                chave="refeicao_nota",
            )
            reflexão_comentário = st.text_input(
                "Compartilhe sua opinião sobre as refeições:",
                chave="refeicao_com",
            )

            st.divider()

            st.markdown("### â 7. Satisfação Geral (NPS)")
            nps = st.radio(
                "Em uma escala de 0 a 10, qual é sua satisfação geral com os serviços de Facilities?",
                opções=lista(intervalo(0, 11)),
                índice=Nenhum,
                horizontal=Verdadeiro,
                chave="nps_nota",
            )

            st.divider()

            st.markdown("### âœ 8. Qual serviço precisa de mais atenção?")
            serviço_atencao = st.multiselect(
                "Selecione um ou mais:",
                opções=SERVIÇOS,
                chave="servico_atencao",
            )

            st.divider()

            st.markdown("### ðŸ“ˆ 9. Percebeu melhoria nos últimos 6 meses?")
            percebeu_melhoria = st.radio(
                "Você viu alguma melhoria nos serviços de Facilities?",
                options=["Sim", "Não", "Não tenho certeza"],
                índice=Nenhum,
                horizontal=Verdadeiro,
                chave="melhoria",
            )

            st.divider()

            st.markdown("### ðŸ'¡ 10. Sugestões")
            sugestões = st.text_area(
                "Deixe suas ideias ou sugestões para aprimorar os serviços:",
                max_chars=1000,
                chave="sugestoes",
            )

            st.divider()

            st.markdown("### ðŸ“ Localização")
            col1, col2 = st.columns(2)

            com col1:
                estados = ibge.listar_estados()
                estado_options = {e["nome"]: e["id"] for e em estados}
                estado = st.selectbox("Estado:", [""] + list(estado_options.keys()))

            com col2:
                município = ""
                se estado:
                    municípios = ibge.listar_municipios(estado_options[estado])
                    mun_nomes = [m["nome"] para m em municípios]
                    município = st.selectbox("Município:", [""] + mun_nomes)
                outro:
                    st.selectbox("Município:", ["Seleção do estado primeiro"])

            st.divider()

            submetido = st.form_submit_button(
                "âœ… Enviar Avaliaçã§çã", use_container_width=True, type="primary"
            )

            se submetido:
                se não estiver em estado:
                    st.error("âš ï¸ Selecione seu estado.")
                outro:
                    dados = {
                        "transporte_nota": transporte_nota,
                        "transporte_comentario": transporte_comentario,
                        "portaria_nota": portaria_nota,
                        "portaria_comentario": portaria_comentario,
                        "vigilância_nota": vigilância_nota,
                        "vigilancia_comentario":vigilancia_comentario,
                        "limpeza_nota": _nota,
                        "limpeza_comentario": limpeza_comentario,
                        "jardinagem_nota": jardinagem_nota,
                        "jardinagem_comentario": jardinagem_comentario,
                        "refeicao_nota": refeicao_nota,
                        "refeicao_comentario": refeicao_comentario,
                        "nps": nps,
                        "servico_atencao": ", ".join(servico_atencao) if servico_atencao else "",
                        "percebeu_melhoria": observar_melhoria,
                        "sugestoes": sugestões,
                        "estado": estado,
                        "município": município,
                        "dados": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    }
                    if smartsheet.enviar_avaliacao(dados):
                        st.session_state.ja_respondeu = True
                        st.success("âœ… Avaliação enviada com sucesso!")
                        st.balloons()
                        st.rerun()
                    outro:
                        st.error("â Œ Erro ao enviar. Tente novamente.")

com tab_resultados:
    st.subheader("ðŸ“Š Painel de Resultados")

    df = smartsheet.buscar_avaliacoes()

    se df.vazio:
        st.info("Nenhuma avaliação registrada ainda.")
    outro:
        notas_cols = [
            "transporte_nota", "portaria_nota", "vigilancia_nota",
            "limpeza_nota", "jardinagem_nota", "refeicao_nota"
        ]
        notas_labels = ["Transporte", "Portaria", "Vigilancia", "Limpeza", "Jardinagem", "Refeicao"]

        para col em notas_cols:
            se col estiver em df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        se "nps" em df.columns:
            df["nps"] = pd.to_numeric(df["nps"], errors="coerce")

        col1, col2, col3, col4 = st.columns(4)
        com col1:
            st.metric("Total de Respostas", len(df))
        com col2:
            media_geral = df[notas_cols].mean().mean()
            st.metric("Mídia Geral", f"{media_geral:.1f}/5")
        com col3:
            se "nps" em df.columns:
                nps_medio = df["nps"].mean()
                st.metric("NPS Medio", f"{nps_medio:.1f}/10")
        com col4:
            melhor_idx = df[notas_cols].mean().idxmax()
            melhor_servico = notas_labels[notas_cols.index(melhor_idx)]
            st.metric("Melhor Avaliado", melhor_servico)

        st.divider()

        medias = [round(df[col].mean(), 2) for col in notas_cols]

        config_radar = {
            "gráfico": {"polar": Verdadeiro, "tipo": "linha"},
            "title": {"text": "Satisfação por Serviço"},
            "painel": {"tamanho": "85%"},
            "xAxis": {"categories": notas_labels, "tickmarkPlacement": "on"},
            "eixoY": {"interpolaçãoLinhaDaGrade": "polígono", "mín": 0, "máx": 5},
            "séries": [{"name": "Media", "data": medias, "pointPlacement": "on"}],
        }
        charts.render_chart(config_radar, height=500)

        ranking_dados = sorted(zip(notas_labels, medias), key=lambda x: x[1], reverse=True)
        gráficos.classificação_barras(
            [r[0] para r em ranking_data],
            [r[1] para r em ranking_data]
        )

        se "nps" em df.columns:
            st.markdown("### Net Promoter Score (NPS)")
            promotores = len(df[df["nps"] >= 9])
            neutros = len(df[(df["nps"] >= 7) & (df["nps"] <= 8)])
            detratores = len(df[df["nps"] <= 6])
            total = len(df)
            nps_score = ((promotores - detratores) / total) * 100

            col1, col2, col3, col4 = st.columns(4)
            com col1:
                st.metric("Promotores (9-10)", promotores)
            com col2:
                st.metric("Neutros (7-8)", neutros)
            com col3:
                st.metric("Detratores (0-6)", detratores)
            com col4:
                st.metric("Pontuação NPS", f"{nps_score:.0f}")

        se "servico_atencao" em df.columns:
            st.markdown("### Serviço que Precisa de Mais Atenção")
            atencao_list = df["servico_atencao"].dropna().str.split(", ").explode()
            se não atencao_list.empty:
                contagem = atencao_list.value_counts()
                config_atencao = {
                    "gráfico": {"tipo": "barra"},
                    "title": {"text": "Serviços que Precisam de Mais Atenção"},
                    "xAxis": {"categories": contagem.index.tolist()},
                    "yAxis": {"title": {"text": "Votos"}},
                    "series": [{"name": "Respostas", "data": [int(v) for v em contagem.values], "showInLegend": False}],
                    "plotOptions": {"bar": {"borderRadius": 5, "dataLabels": {"enabled": True}}},
                }
                charts.render_chart(config_atencao)

        if "percebeu_melhoria" em df.columns:
            st.markdown("### Percebeu Melhoria nos Últimos 6 Meses?")
            melhoria_count = df["percebeu_melhoria"].value_counts()
            config_melhoria = {
                "gráfico": {"tipo": "pizza"},
                "title": {"text": "Percepção de Melhoria"},
                "plotOptions": {"pie": {"innerSize": "50%", "dataLabels": {"enabled": True, "format": "{point.name}: {point.percentage:.1f}%"}}},
                "série": [{"nome": "Respostas", "dados": [
                    {"name": str(nome), "y": int(qtd)} para nome, qtd em melhoria_count.items()
                ]}],
            }
            charts.render_chart(config_melhoria)