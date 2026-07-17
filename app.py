# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
from datetime import datetime

from modules.smartsheet_api import SmartsheetManager
from modules.ibge_api import IBGEService

try:
    from config import PAINEL_SENHA
except Exception:
    PAINEL_SENHA = None


# =====================================================
# CONFIGURAÇÃO DA PÁGINA
# =====================================================
st.set_page_config(
    page_title="Pesquisa de Satisfação - Facilities",
    page_icon="📋",
    layout="wide",
)


# =====================================================
# ESTILO VISUAL
# =====================================================
st.markdown(
    """
    <style>
        .main-header {
            background: linear-gradient(135deg, #003B7A 0%, #002060 100%);
            color: white;
            padding: 42px 48px;
            border-radius: 12px;
            border-left: 8px solid #00A651;
            margin-bottom: 28px;
        }
        .main-header h1 {
            font-size: 42px;
            margin-bottom: 12px;
        }
        .main-header p {
            font-size: 17px;
            margin-bottom: 18px;
        }
        .anonymous-badge {
            background: #00A651;
            color: white;
            padding: 8px 18px;
            border-radius: 20px;
            font-weight: 600;
            display: inline-block;
        }
        .intro-box {
            background: #F5F7FA;
            border-left: 5px solid #00A651;
            padding: 24px 28px;
            border-radius: 10px;
            margin-bottom: 24px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="main-header">
        <h1>Pesquisa de Satisfação</h1>
        <p>Syngenta Brasil · Serviços de Facilities · 1º Semestre 2026</p>
        <span class="anonymous-badge">🔒 100% Anônimo</span>
    </div>
    """,
    unsafe_allow_html=True,
)


# =====================================================
# INTEGRAÇÕES
# =====================================================
smartsheet = SmartsheetManager()
ibge = IBGEService()


# =====================================================
# ESCALAS E CAMPOS
# =====================================================
ESCALA_1_5 = {
    1: "1 - Ruim",
    2: "2 - Regular",
    3: "3 - Bom",
    4: "4 - Ótimo",
    5: "5 - Excelente",
}

SERVICOS_ATENCAO = [
    "Portaria",
    "Transporte",
    "Refeição",
    "Limpeza",
    "Jardinagem",
]

COLUNAS_NOTA = [
    "transporte_pontualidade_nota",
    "transporte_conforto_limpeza_nota",
    "portaria_atendimento_nota",
    "portaria_controle_acesso_seguranca_nota",
    "refeicao_qualidade_nota",
    "refeicao_variedade_cardapio_nota",
    "limpeza_instalacoes_nota",
    "jardinagem_areas_externas_nota",
    "facilities_geral_nota",
]

LABELS_NOTA = [
    "Pontualidade do transporte",
    "Conforto e limpeza dos veículos",
    "Atendimento da portaria",
    "Controle de acesso e segurança",
    "Qualidade das refeições",
    "Variedade do cardápio",
    "Limpeza das instalações",
    "Áreas externas e jardins",
    "Facilities geral",
]


# =====================================================
# ABAS
# =====================================================
tab_formulario, tab_resultados = st.tabs([
    "📝 Formulário de Avaliação",
    "📊 Painel de Resultados",
])


# =====================================================
# FORMULÁRIO
# =====================================================
with tab_formulario:
    if "ja_respondeu" not in st.session_state:
        st.session_state.ja_respondeu = False

    if st.session_state.ja_respondeu:
        st.success("✅ Sua avaliação foi enviada com sucesso. Obrigada pela participação!")
        st.info("Para preservar a integridade da pesquisa, cada pessoa deve responder apenas uma vez nesta sessão.")

    else:
        st.markdown(
            """
            <div class="intro-box">
                <p><strong>Prezada(o) colaboradora(or),</strong></p>
                <p>
                    Sua opinião é essencial para a melhoria contínua dos nossos serviços de Facilities.
                    Por favor, avalie os aspectos abaixo utilizando a seguinte escala:
                </p>
                <p><strong>1 = Ruim | 2 = Regular | 3 = Bom | 4 = Ótimo | 5 = Excelente</strong></p>
                <p>Basta selecionar a opção que melhor representa sua experiência em cada pergunta.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.form("form_pesquisa_facilities", clear_on_submit=True):
            st.markdown("### 🚌 Transporte")

            transporte_pontualidade_nota = st.radio(
                "Como você avalia a pontualidade do transporte?",
                options=[1, 2, 3, 4, 5],
                index=None,
                format_func=lambda x: ESCALA_1_5[x],
                horizontal=True,
                key="transporte_pontualidade_nota",
            )

            transporte_conforto_limpeza_nota = st.radio(
                "Como você avalia o conforto e a limpeza dos veículos?",
                options=[1, 2, 3, 4, 5],
                index=None,
                format_func=lambda x: ESCALA_1_5[x],
                horizontal=True,
                key="transporte_conforto_limpeza_nota",
            )

            transporte_comentarios = st.text_area(
                "Compartilhe seus comentários ou sugestões sobre o serviço de transporte:",
                placeholder="Insira sua resposta",
                max_chars=1000,
                key="transporte_comentarios",
            )

            st.divider()

            st.markdown("### 🚪 Portaria")

            portaria_atendimento_nota = st.radio(
                "Como você avalia o atendimento da portaria?",
                options=[1, 2, 3, 4, 5],
                index=None,
                format_func=lambda x: ESCALA_1_5[x],
                horizontal=True,
                key="portaria_atendimento_nota",
            )

            portaria_controle_acesso_seguranca_nota = st.radio(
                "Como você avalia o controle de acesso e a segurança no site?",
                options=[1, 2, 3, 4, 5],
                index=None,
                format_func=lambda x: ESCALA_1_5[x],
                horizontal=True,
                key="portaria_controle_acesso_seguranca_nota",
            )

            portaria_comentarios = st.text_area(
                "Compartilhe sua opinião sobre a portaria: elogios, críticas ou sugestões.",
                placeholder="Insira sua resposta",
                max_chars=1000,
                key="portaria_comentarios",
            )

            st.divider()

            st.markdown("### 🍽️ Refeição")

            refeicao_qualidade_nota = st.radio(
                "Como você avalia a qualidade das refeições servidas?",
                options=[1, 2, 3, 4, 5],
                index=None,
                format_func=lambda x: ESCALA_1_5[x],
                horizontal=True,
                key="refeicao_qualidade_nota",
            )

            refeicao_variedade_cardapio_nota = st.radio(
                "Como você avalia a variedade do cardápio oferecido?",
                options=[1, 2, 3, 4, 5],
                index=None,
                format_func=lambda x: ESCALA_1_5[x],
                horizontal=True,
                key="refeicao_variedade_cardapio_nota",
            )

            refeicao_comentarios = st.text_area(
                "Compartilhe sua opinião sobre as refeições: elogios, críticas ou sugestões.",
                placeholder="Insira sua resposta",
                max_chars=1000,
                key="refeicao_comentarios",
            )

            st.divider()

            st.markdown("### 🧹 Limpeza e Jardinagem")

            limpeza_instalacoes_nota = st.radio(
                "Como você avalia a limpeza das instalações, como escritórios, banheiros e áreas comuns?",
                options=[1, 2, 3, 4, 5],
                index=None,
                format_func=lambda x: ESCALA_1_5[x],
                horizontal=True,
                key="limpeza_instalacoes_nota",
            )

            jardinagem_areas_externas_nota = st.radio(
                "Como você avalia a conservação das áreas externas e jardins?",
                options=[1, 2, 3, 4, 5],
                index=None,
                format_func=lambda x: ESCALA_1_5[x],
                horizontal=True,
                key="jardinagem_areas_externas_nota",
            )

            limpeza_jardinagem_comentarios = st.text_area(
                "Compartilhe sua opinião sobre limpeza e jardinagem: elogios, críticas ou sugestões.",
                placeholder="Insira sua resposta",
                max_chars=1000,
                key="limpeza_jardinagem_comentarios",
            )

            st.divider()

            st.markdown("### 📋 Avaliação Geral")

            nps_satisfacao_geral = st.radio(
                "Em uma escala de 0 a 10, onde 0 significa 'nada satisfeita(o)' e 10 'extremamente satisfeita(o)', qual é sua satisfação geral com os serviços de Facilities?",
                options=list(range(0, 11)),
                index=None,
                horizontal=True,
                key="nps_satisfacao_geral",
            )

            facilities_geral_nota = st.radio(
                "Como você avalia os serviços de Facilities de forma geral?",
                options=[1, 2, 3, 4, 5],
                index=None,
                format_func=lambda x: ESCALA_1_5[x],
                horizontal=True,
                key="facilities_geral_nota",
            )

            servico_precisa_atencao = st.multiselect(
                "Na sua opinião, quais serviços precisam de mais atenção ou melhorias?",
                options=SERVICOS_ATENCAO,
                key="servico_precisa_atencao",
            )

            st.divider()

            st.markdown("### 💬 Comentários e Sugestões")

            comentarios_sugestoes = st.text_area(
                "Deixe aqui seus comentários, elogios ou sugestões de melhoria:",
                placeholder="Insira sua resposta",
                max_chars=1500,
                key="comentarios_sugestoes",
            )

            st.divider()

            st.markdown("### 📍 Localização")
            col1, col2 = st.columns(2)

            with col1:
                estados = ibge.listar_estados()
                estado_options = {e["nome"]: e["id"] for e in estados}
                estado = st.selectbox("Estado:", [""] + list(estado_options.keys()))

            with col2:
                municipio = ""
                if estado:
                    municipios = ibge.listar_municipios(estado_options[estado])
                    municipio_options = [m["nome"] for m in municipios]
                    municipio = st.selectbox("Município:", [""] + municipio_options)
                else:
                    st.selectbox("Município:", ["Selecione o estado primeiro"])

            st.divider()

            submitted = st.form_submit_button(
                "✅ Enviar avaliação",
                use_container_width=True,
                type="primary",
            )

            if submitted:
                campos_obrigatorios = {
                    "Pontualidade do transporte": transporte_pontualidade_nota,
                    "Conforto e limpeza dos veículos": transporte_conforto_limpeza_nota,
                    "Atendimento da portaria": portaria_atendimento_nota,
                    "Controle de acesso e segurança": portaria_controle_acesso_seguranca_nota,
                    "Qualidade das refeições": refeicao_qualidade_nota,
                    "Variedade do cardápio": refeicao_variedade_cardapio_nota,
                    "Limpeza das instalações": limpeza_instalacoes_nota,
                    "Conservação das áreas externas e jardins": jardinagem_areas_externas_nota,
                    "Satisfação geral 0 a 10": nps_satisfacao_geral,
                    "Avaliação geral de Facilities": facilities_geral_nota,
                    "Estado": estado,
                    "Município": municipio,
                }

                pendentes = [nome for nome, valor in campos_obrigatorios.items() if valor in [None, ""]]

                if pendentes:
                    st.error("⚠️ Preencha os campos obrigatórios antes de enviar: " + ", ".join(pendentes))
                else:
                    dados = {
                        "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "estado": estado,
                        "municipio": municipio,
                        "transporte_pontualidade_nota": transporte_pontualidade_nota,
                        "transporte_conforto_limpeza_nota": transporte_conforto_limpeza_nota,
                        "transporte_comentarios": transporte_comentarios,
                        "portaria_atendimento_nota": portaria_atendimento_nota,
                        "portaria_controle_acesso_seguranca_nota": portaria_controle_acesso_seguranca_nota,
                        "portaria_comentarios": portaria_comentarios,
                        "refeicao_qualidade_nota": refeicao_qualidade_nota,
                        "refeicao_variedade_cardapio_nota": refeicao_variedade_cardapio_nota,
                        "refeicao_comentarios": refeicao_comentarios,
                        "limpeza_instalacoes_nota": limpeza_instalacoes_nota,
                        "jardinagem_areas_externas_nota": jardinagem_areas_externas_nota,
                        "limpeza_jardinagem_comentarios": limpeza_jardinagem_comentarios,
                        "nps_satisfacao_geral": nps_satisfacao_geral,
                        "facilities_geral_nota": facilities_geral_nota,
                        "servico_precisa_atencao": ", ".join(servico_precisa_atencao) if servico_precisa_atencao else "",
                        "comentarios_sugestoes": comentarios_sugestoes,
                    }

                    if smartsheet.enviar_avaliacao(dados):
                        st.session_state.ja_respondeu = True
                        st.success("✅ Avaliação enviada com sucesso!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("❌ Erro ao enviar a avaliação. Verifique a conexão com o Smartsheet e os nomes das colunas.")


# =====================================================
# PAINEL DE RESULTADOS RESTRITO
# =====================================================
with tab_resultados:
    st.subheader("🔒 Painel de Resultados - Área Restrita")
    st.warning("Este painel é restrito à equipe responsável pela pesquisa.")

    if "painel_liberado" not in st.session_state:
        st.session_state.painel_liberado = False

    if not st.session_state.painel_liberado:
        senha_digitada = st.text_input(
            "Digite a senha para acessar o painel de resultados:",
            type="password",
            key="senha_painel_resultados",
        )

        if st.button("Acessar painel", type="primary"):
            if not PAINEL_SENHA:
                st.error("Senha do painel não configurada. Adicione PAINEL_SENHA no arquivo config.py.")
            elif senha_digitada == PAINEL_SENHA:
                st.session_state.painel_liberado = True
                st.rerun()
            else:
                st.error("Senha incorreta. Acesso não autorizado.")

        st.stop()

    st.success("Acesso autorizado.")
    st.subheader("📊 Dashboard de Resultados")

    df = smartsheet.buscar_avaliacoes()

    if df.empty:
        st.info("Nenhuma avaliação registrada ainda.")
    else:
        for col in COLUNAS_NOTA:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        if "nps_satisfacao_geral" in df.columns:
            df["nps_satisfacao_geral"] = pd.to_numeric(df["nps_satisfacao_geral"], errors="coerce")

        colunas_existentes = [col for col in COLUNAS_NOTA if col in df.columns]
        labels_existentes = [LABELS_NOTA[COLUNAS_NOTA.index(col)] for col in colunas_existentes]

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total de respostas", len(df))

        with col2:
            if colunas_existentes:
                media_servicos = df[colunas_existentes].mean().mean()
                st.metric("Média dos serviços", f"{media_servicos:.1f}/5")
            else:
                st.metric("Média dos serviços", "-")

        with col3:
            if "facilities_geral_nota" in df.columns:
                media_facilities = df["facilities_geral_nota"].mean()
                st.metric("Facilities geral", f"{media_facilities:.1f}/5")
            else:
                st.metric("Facilities geral", "-")

        with col4:
            if "nps_satisfacao_geral" in df.columns:
                media_nps = df["nps_satisfacao_geral"].mean()
                st.metric("Satisfação 0 a 10", f"{media_nps:.1f}/10")
            else:
                st.metric("Satisfação 0 a 10", "-")

        st.divider()

        if colunas_existentes:
            medias = [round(df[col].mean(), 2) for col in colunas_existentes]
            ranking = pd.DataFrame({
                "Item avaliado": labels_existentes,
                "Nota média": medias,
            }).sort_values("Nota média", ascending=False)

            st.markdown("### Média por item avaliado")
            st.bar_chart(ranking.set_index("Item avaliado"))

            st.markdown("### Ranking de avaliação")
            st.dataframe(ranking, use_container_width=True, hide_index=True)

        if "nps_satisfacao_geral" in df.columns:
            st.markdown("### Satisfação geral - escala 0 a 10")

            nps_validos = df["nps_satisfacao_geral"].dropna()
            if not nps_validos.empty:
                promotores = len(nps_validos[nps_validos >= 9])
                neutros = len(nps_validos[(nps_validos >= 7) & (nps_validos <= 8)])
                detratores = len(nps_validos[nps_validos <= 6])
                total_nps = len(nps_validos)
                nps_score = ((promotores - detratores) / total_nps) * 100 if total_nps > 0 else 0

                c1, c2, c3, c4 = st.columns(4)
                with c1:
                    st.metric("Promotores", promotores)
                with c2:
                    st.metric("Neutros", neutros)
                with c3:
                    st.metric("Detratores", detratores)
                with c4:
                    st.metric("NPS", f"{nps_score:.0f}")

                nps_dist = nps_validos.value_counts().sort_index()
                st.bar_chart(nps_dist)

        if "servico_precisa_atencao" in df.columns:
            st.markdown("### Serviços que precisam de mais atenção")

            atencao = df["servico_precisa_atencao"].dropna().astype(str).str.split(", ").explode()
            atencao = atencao[atencao != ""]

            if not atencao.empty:
                contagem = atencao.value_counts()
                st.bar_chart(contagem)
            else:
                st.info("Ainda não há marcações de serviços que precisam de atenção.")

        with st.expander("Ver dados coletados"):
            st.dataframe(df, use_container_width=True)
