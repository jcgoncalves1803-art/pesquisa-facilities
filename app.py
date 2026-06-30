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

header_html = '<div style="text-align:center; padding:20px; background:linear-gradient(135deg,#1a1a2e,#0f3460); color:white; border-radius:12px; margin-bottom:25px;">'
header_html += '<img src="https://logospng.org/download/syngenta/syngenta-4096.png" alt="Syngenta" style="height:50px; margin-bottom:15px;">'
header_html += '<h1>Pesquisa de Satisfação</h1>'
header_html += '<h3>Serviços de Instalações | 1º semestre de 2026</h3>'
header_html += '<p>Avalie sua satisfação com transporte, portaria, vigilância, limpeza, jardinagem e refeicao</p>'
header_html += '<span style="background:#28a745; padding:5px 15px; border-radius:20px; font-size:0.85em;">100% Anônimo</span>'
header_html += '</div>'
st.markdown(header_html, unsafe_allow_html=True)

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

tab_avaliar, tab_resultados = st.tabs(["Avaliar", "Resultados"])

com tab_avaliar:
    se "ja_respondeu" não estiver em st.session_state:
        st.session_state.ja_respondeu = Falso

    se st.session_state.ja_respondeu:
        st.success("Você já está com inveja de sua avaliação. Obrigado pela participação!")
        st.info("Cada pessoa pode responder apenas uma vez.")
    outro:
        st.markdown("**Prezado(a) colaborador(a),**")
        st.markdown("Sua opinião e essencial para a melhoria contínua dos nossos serviços de Facilities.")
        st.markdown("Por favor, avalie os aspectos abaixo utilizando a seguinte escala:")
        st.markdown("1 - Muito insatisfeito | 2 - Insatisfeito | 3 - Neutro | 4 - Satisfeito | 5 - Muito satisfeito")

        st.divider()

        com st.form("form_avaliacao", clear_on_submit=True):

            st.markdown("### 1. Transporte")
            transporte_nota = st.radio(
                "Qual sua satisfação com o serviço de transporte?",
                opções=[1, 2, 3, 4, 5],
                formato_func=lambda x: ESCALA[x],
                horizontal=Verdadeiro,
                chave="transporte_nota",
            )
            transporte_comentário = st.text_input(
                "Compartilhe seus comentários sobre o transporte:",
                chave="transporte_com",
            )

            st.divider()

            st.markdown("### 2. Portaria")
            portaria_nota = st.radio(
                "Qual sua satisfação com o serviço de portaria?",
                opções=[1, 2, 3, 4, 5],
                formato_func=lambda x: ESCALA[x],
                horizontal=Verdadeiro,
                chave="portaria_nota",
            )
            portaria_comentario = st.text_input(
                "Compartilhe sua opinião sobre a portaria:",
                chave="portaria_com",
            )

            st.divider()

            st.markdown("### 3. Vigilância")
            vigilância_nota = st.radio(
                "Qual sua satisfação com o serviço de vigilância?",
                opções=[1, 2, 3, 4, 5],
                formato_func=lambda x: ESCALA[x],
                horizontal=Verdadeiro,
                chave="vigilância_nota",
            )
            vigilante_comentario = st.text_input(
                "Compartilhe sua opinião sobre a vigilância:",
                chave="vigilância_com",
            )

            st.divider()

            st.markdown("### 4. Limpeza")
            …_nota = st.radio(
                "Qual sua satisfação com o serviço de limpeza?",
                opções=[1, 2, 3, 4, 5],
                formato_func=lambda x: ESCALA[x],
                horizontal=Verdadeiro,
                chave="limpeza_nota",
            )
            limpeza_comentário = st.text_input(
                "Compartilhe sua opinião sobre a limpeza:",
                chave="limpeza_com",
            )

            st.divider()

            st.markdown("### 5. Jardinagem")
            cultivar_nota = st.radio(
                "Qual sua satisfação com o serviço de jardinagem?",
                opções=[1, 2, 3, 4, 5],
                formato_func=lambda x: ESCALA[x],
                horizontal=Verdadeiro,
                chave="jardinagem_nota",
            )
            jardinagem_comentário = st.text_input(
                "Compartilhe sua opinião sobre a jardinagem:",
                chave="jardinagem_com",
            )

            st.divider()

            st.markdown("### 6. Refeição")
            refeicao_nota = st.radio(
                "Qual sua satisfação com o serviço de refeição?",
                opções=[1, 2, 3, 4, 5],
                formato_func=lambda x: ESCALA[x],
                horizontal=Verdadeiro,
                chave="refeicao_nota",
            )
            reflexão_comentário = st.text_input(
                "Compartilhe sua opinião sobre as refeições:",
                chave="refeicao_com",
            )

            st.divider()

            st.markdown("### 7. Satisfação Geral (NPS)")
            nps = st.slider(
                "Em uma escala de 0 a 10, qual é sua satisfação geral com os serviços de Facilities?",
                valor_mínimo=0,
                valor_máximo=10,
                valor=5,
                chave="nps",
            )

            st.divider()

            st.markdown("### 8. Qual serviço precisa de mais atenção?")
            serviço_atencao = st.multiselect(
                "Selecione um ou mais:",
                opções=SERVIÇOS,
                chave="servico_atencao",
            )

            st.divider()

            st.markdown("### 9. Percebeu melhoria nos últimos 6 meses?")
            percebeu_melhoria = st.radio(
                "Você está vendo alguma melhoria nos serviços de Instalações?",
                options=["Sim", "Nao", "Não tenho certeza"],
                horizontal=Verdadeiro,
                chave="melhoria",
            )

            st.divider()

            st.markdown("### 10. Sugestões")
            sugestões = st.text_area(
                "Deixe suas ideias ou sugestões para aprimorar os serviços:",
                max_chars=1000,
                chave="sugestoes",
            )

            st.divider()

            st.markdown("### Localização")
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
                "Enviar Avaliacao", use_container_width=True, type="primary"
            )

            se submetido:
                se não estiver em estado:
                    st.error("Selecione seu estado.")
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
                        st.success("Avaliação enviada com sucesso!")
                        st.balloons()
                        st.rerun()
                    outro:
                        st.error("Erro ao enviar. Tente novamente.")

com tab_resultados:
    st.subheader("Painel de Resultados")

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

        se "nps" em df.columns:
            charts.gauge_nps(df["nps"].mean())

        medias = [round(df[col].mean(), 2) for col in notas_cols]
        gráficos.teia_de_aranha(rótulos_de_notas, mídias)
        charts.column_drilldown(notas_labels, medias)

        dados_empilhados = {}
        para nota em [1, 2, 3, 4, 5]:
            dados_stacked[nota] = [int((df[col] == nota).sum()) for col in notas_cols]
        gráficos.barras_empilhadas(rótulos_notas, dados_empilhados)

        ranking_dados = sorted(zip(notas_labels, medias), key=lambda x: x[1], reverse=True)
        gráficos.classificação_barras(
            [r[0] para r em ranking_data],
            [r[1] para r em ranking_data]
        )

        dados_servicos = {}
        para rótulo, coluna em zip(notas_labels, notas_cols):
            se col estiver em df.columns:
                dados_servicos[rótulo] = round(df[col].mean(), 2)
        se dados_servicos:
            charts.bar_race(dados_servicos)

        se "servico_atencao" em df.columns:
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
