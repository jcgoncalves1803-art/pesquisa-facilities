# -*- coding: utf-8 -*-

import os
from datetime import datetime

import altair as alt
import pandas as pd
import streamlit as st

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

        button[kind="primary"],
        button[data-testid="stBaseButton-primary"] {
            background-color: #002B7F !important;
            color: white !important;
            border: 2px solid #00A651 !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
        }

        button[kind="primary"]:hover,
        button[data-testid="stBaseButton-primary"]:hover {
            background-color: #001F5C !important;
            border-color: #00A651 !important;
            color: white !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# =====================================================
# LOGO
# =====================================================
LOGO_PATH = "assets/logo_syngenta.png"

try:
    if os.path.exists(LOGO_PATH):
        coluna_esquerda, coluna_logo, coluna_direita = st.columns([1, 1, 1])

        with coluna_logo:
            st.image(LOGO_PATH, width=230)

except Exception:
    st.warning("A logo não pôde ser carregada. O formulário continuará disponível.")


# =====================================================
# CABEÇALHO
# =====================================================
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
# CONFIGURAÇÕES
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
    "Fretado",
    "Refeição",
    "Limpeza",
    "Jardinagem",
]

COLUNAS_NOTA = [
    "transporte_pontualidade_nota",
    "transporte_conforto_limpeza_nota",
    "seguranca_veicular_nota",
    "portaria_atendimento_nota",
    "portaria_controle_acesso_seguranca_nota",
    "refeicao_qualidade_nota",
    "refeicao_variedade_cardapio_nota",
    "limpeza_instalacoes_nota",
    "jardinagem_areas_externas_nota",
    "facilities_geral_nota",
]

LABELS_NOTA = [
    "Pontualidade do fretado",
    "Conforto e limpeza dos veículos",
    "Segurança durante o deslocamento",
    "Atendimento da portaria",
    "Controle de acesso e segurança",
    "Qualidade das refeições",
    "Variedade do cardápio",
    "Limpeza das instalações",
    "Áreas externas e jardins",
    "Facilities geral",
]

CORES_AREAS = {
    "Fretado": "#334C56",
    "Portaria": "#264600",
    "Refeição": "#00A0BE",
    "Limpeza": "#6F0055",
    "Jardinagem": "#7D7D7D",
    "Facilities geral": "#002060",
}


# =====================================================
# FUNÇÕES
# =====================================================
def campo_vazio(valor):
    if valor is None or valor == "" or valor == []:
        return True

    if isinstance(valor, str) and valor.strip() == "":
        return True

    return False


def pergunta_nota(pergunta, chave):
    return st.radio(
        pergunta,
        options=[1, 2, 3, 4, 5],
        index=None,
        format_func=lambda x: ESCALA_1_5[x],
        horizontal=True,
        key=chave,
    )


def definir_area(item):
    if item in [
        "Pontualidade do fretado",
        "Conforto e limpeza dos veículos",
        "Segurança durante o deslocamento",
    ]:
        return "Fretado"

    if item in [
        "Atendimento da portaria",
        "Controle de acesso e segurança",
    ]:
        return "Portaria"

    if item in [
        "Qualidade das refeições",
        "Variedade do cardápio",
    ]:
        return "Refeição"

    if item == "Limpeza das instalações":
        return "Limpeza"

    if item == "Áreas externas e jardins":
        return "Jardinagem"

    return "Facilities geral"


# =====================================================
# ABAS
# =====================================================
tab_formulario, tab_resultados = st.tabs(
    [
        "📝 Formulário de Avaliação",
        "📊 Painel de Resultados",
    ]
)


# =====================================================
# FORMULÁRIO
# =====================================================
with tab_formulario:
    if "ja_respondeu" not in st.session_state:
        st.session_state.ja_respondeu = False

    if st.session_state.ja_respondeu:
        st.success("✅ Sua avaliação foi enviada com sucesso. Obrigada pela participação!")
        st.info("Cada pessoa deve responder apenas uma vez nesta sessão.")

    else:
        st.markdown(
            """
            <div class="intro-box">
                <p><strong>Prezado(a) colaborador(a),</strong></p>
                <p>
                    Sua opinião é essencial para a melhoria contínua dos nossos
                    serviços de Facilities. Por favor, avalie os aspectos abaixo
                    utilizando a seguinte escala:
                </p>
                <p>
                    <strong>
                        1 = Ruim | 2 = Regular | 3 = Bom |
                        4 = Ótimo | 5 = Excelente
                    </strong>
                </p>
                <p>
                    Basta selecionar a opção que melhor representa sua experiência
                    em cada pergunta.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # FRETADO
        st.markdown("### 🚌 Transporte de Colaboradores (Fretado)")

        transporte_pontualidade_nota = pergunta_nota(
            "Como você avalia a pontualidade do transporte de colaboradores?",
            "transporte_pontualidade_nota",
        )

        transporte_conforto_limpeza_nota = pergunta_nota(
            "Como você avalia o conforto e a limpeza dos veículos do fretado?",
            "transporte_conforto_limpeza_nota",
        )

        seguranca_veicular_nota = pergunta_nota(
            "Como você avalia sua sensação de segurança durante o deslocamento no fretado?",
            "seguranca_veicular_nota",
        )

        transporte_comentarios = st.text_area(
            "Compartilhe seus comentários ou sugestões sobre o serviço de fretado:",
            placeholder="Insira sua resposta",
            max_chars=1000,
            key="transporte_comentarios",
        )

        st.info(
            "Atenção: situações de risco, emergência ou incidentes devem ser comunicados pelos canais oficiais de segurança "
            "do site. Não utilize esta pesquisa para esse tipo de reporte."
        )

        st.divider()

        # PORTARIA
        st.markdown("### 🚪 Portaria")

        portaria_atendimento_nota = pergunta_nota(
            "Como você avalia o atendimento da portaria?",
            "portaria_atendimento_nota",
        )

        portaria_controle_acesso_seguranca_nota = pergunta_nota(
            "Como você avalia o controle de acesso e a segurança no site?",
            "portaria_controle_acesso_seguranca_nota",
        )

        portaria_comentarios = st.text_area(
            "Compartilhe sua opinião sobre a portaria: elogios, críticas ou sugestões.",
            placeholder="Insira sua resposta",
            max_chars=1000,
            key="portaria_comentarios",
        )

        st.divider()

        # REFEIÇÃO
        st.markdown("### 🍽️ Refeição")

        refeicao_qualidade_nota = pergunta_nota(
            "Como você avalia a qualidade das refeições servidas?",
            "refeicao_qualidade_nota",
        )

        refeicao_variedade_cardapio_nota = pergunta_nota(
            "Como você avalia a variedade do cardápio oferecido?",
            "refeicao_variedade_cardapio_nota",
        )

        refeicao_comentarios = st.text_area(
            "Compartilhe sua opinião sobre as refeições: elogios, críticas ou sugestões.",
            placeholder="Insira sua resposta",
            max_chars=1000,
            key="refeicao_comentarios",
        )

        st.divider()

        # LIMPEZA E JARDINAGEM
        st.markdown("### 🧹 Limpeza e Jardinagem")

        limpeza_instalacoes_nota = pergunta_nota(
            "Como você avalia a limpeza das instalações, como escritórios, banheiros e áreas comuns?",
            "limpeza_instalacoes_nota",
        )

        jardinagem_areas_externas_nota = pergunta_nota(
            "Como você avalia a conservação das áreas externas e jardins?",
            "jardinagem_areas_externas_nota",
        )

        limpeza_jardinagem_comentarios = st.text_area(
            "Compartilhe sua opinião sobre limpeza e jardinagem: elogios, críticas ou sugestões.",
            placeholder="Insira sua resposta",
            max_chars=1000,
            key="limpeza_jardinagem_comentarios",
        )

        st.divider()

        # AVALIAÇÃO GERAL
        st.markdown("### 📋 Avaliação Geral")

        nps_satisfacao_geral = st.radio(
            "Em uma escala de 0 a 10, onde 0 significa 'nada satisfeita(o)' "
            "e 10 'extremamente satisfeita(o)', qual é sua satisfação geral "
            "com os serviços de Facilities?",
            options=list(range(0, 11)),
            index=None,
            horizontal=True,
            key="nps_satisfacao_geral",
        )

        facilities_geral_nota = pergunta_nota(
            "Como você avalia os serviços de Facilities de forma geral?",
            "facilities_geral_nota",
        )

        servico_precisa_atencao = st.multiselect(
            "Na sua opinião, quais serviços precisam de mais atenção ou melhorias? *",
            options=SERVICOS_ATENCAO,
            key="servico_precisa_atencao",
        )

        st.divider()

        # COMENTÁRIOS
        st.markdown("### 💬 Comentários e Sugestões")

        comentarios_sugestoes = st.text_area(
            "Deixe aqui seus comentários, elogios ou sugestões de melhoria: *",
            placeholder="Campo obrigatório",
            max_chars=1500,
            key="comentarios_sugestoes",
        )

        st.divider()

        # LOCALIZAÇÃO
        st.markdown("### 📍 Localização")

        coluna_estado, coluna_municipio = st.columns(2)

        with coluna_estado:
            estados = ibge.listar_estados()
            estado_options = {e["nome"]: e["id"] for e in estados}

            estado = st.selectbox(
                "Estado:",
                [""] + list(estado_options.keys()),
                key="estado_select",
            )

        with coluna_municipio:
            if estado:
                municipios = ibge.listar_municipios(estado_options[estado])
                municipio_options = [m["nome"] for m in municipios]

                municipio = st.selectbox(
                    "Município:",
                    [""] + municipio_options,
                    key="municipio_select",
                )
            else:
                municipio = ""

                st.selectbox(
                    "Município:",
                    ["Selecione o estado primeiro"],
                    key="municipio_select_placeholder",
                )

        st.divider()

        submitted = st.button(
            "✅ Enviar avaliação",
            use_container_width=True,
            type="primary",
        )

        if submitted:
            campos_obrigatorios = {
                "Pontualidade do fretado": transporte_pontualidade_nota,
                "Conforto e limpeza dos veículos do fretado": transporte_conforto_limpeza_nota,
                "Segurança durante o deslocamento no fretado": seguranca_veicular_nota,
                "Atendimento da portaria": portaria_atendimento_nota,
                "Controle de acesso e segurança": portaria_controle_acesso_seguranca_nota,
                "Qualidade das refeições": refeicao_qualidade_nota,
                "Variedade do cardápio": refeicao_variedade_cardapio_nota,
                "Limpeza das instalações": limpeza_instalacoes_nota,
                "Conservação das áreas externas e jardins": jardinagem_areas_externas_nota,
                "Satisfação geral de 0 a 10": nps_satisfacao_geral,
                "Avaliação geral de Facilities": facilities_geral_nota,
                "Serviço que precisa de mais atenção": servico_precisa_atencao,
                "Comentários e sugestões gerais": comentarios_sugestoes,
                "Estado": estado,
                "Município": municipio,
            }

            pendentes = [
                nome
                for nome, valor in campos_obrigatorios.items()
                if campo_vazio(valor)
            ]

            if pendentes:
                st.error(
                    "⚠️ Preencha os campos obrigatórios antes de enviar: "
                    + ", ".join(pendentes)
                )

            else:
                dados = {
                    "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "estado": estado,
                    "municipio": municipio,
                    "transporte_pontualidade_nota": transporte_pontualidade_nota,
                    "transporte_conforto_limpeza_nota": transporte_conforto_limpeza_nota,
                    "seguranca_veicular_nota": seguranca_veicular_nota,
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
                    "servico_precisa_atencao": ", ".join(servico_precisa_atencao),
                    "comentarios_sugestoes": comentarios_sugestoes,
                }

                if smartsheet.enviar_avaliacao(dados):
                    st.session_state.ja_respondeu = True
                    st.success("✅ Avaliação enviada com sucesso!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error(
                        "❌ Erro ao enviar a avaliação. Verifique a conexão com "
                        "o Smartsheet e os nomes das colunas."
                    )


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
                st.error(
                    "Senha do painel não configurada. "
                    "Adicione PAINEL_SENHA no arquivo config.py."
                )
            elif senha_digitada == PAINEL_SENHA:
                st.session_state.painel_liberado = True
                st.rerun()
            else:
                st.error("Senha incorreta. Acesso não autorizado.")

    else:
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
                df["nps_satisfacao_geral"] = pd.to_numeric(
                    df["nps_satisfacao_geral"],
                    errors="coerce",
                )

            colunas_existentes = [
                col
                for col in COLUNAS_NOTA
                if col in df.columns
            ]

            labels_existentes = [
                LABELS_NOTA[COLUNAS_NOTA.index(col)]
                for col in colunas_existentes
            ]

            c1, c2, c3, c4 = st.columns(4)

            with c1:
                st.metric("Total de respostas", len(df))

            with c2:
                if colunas_existentes:
                    media_servicos = df[colunas_existentes].mean().mean()
                    st.metric("Média dos serviços", f"{media_servicos:.1f}/5")
                else:
                    st.metric("Média dos serviços", "-")

            with c3:
                if "facilities_geral_nota" in df.columns:
                    media_facilities = df["facilities_geral_nota"].mean()
                    st.metric("Facilities geral", f"{media_facilities:.1f}/5")
                else:
                    st.metric("Facilities geral", "-")

            with c4:
                if "nps_satisfacao_geral" in df.columns:
                    media_nps = df["nps_satisfacao_geral"].mean()
                    st.metric("Satisfação 0 a 10", f"{media_nps:.1f}/10")
                else:
                    st.metric("Satisfação 0 a 10", "-")

            st.divider()

            # GRÁFICO DE MÉDIAS
            if colunas_existentes:
                medias = [
                    round(df[col].mean(), 2)
                    for col in colunas_existentes
                ]

                ranking = pd.DataFrame(
                    {
                        "Item avaliado": labels_existentes,
                        "Nota média": medias,
                    }
                )

                ranking["Área"] = ranking["Item avaliado"].apply(definir_area)

                st.markdown("### Média por item avaliado")

                grafico_medias = (
                    alt.Chart(ranking)
                    .mark_bar(
                        cornerRadiusTopLeft=6,
                        cornerRadiusTopRight=6,
                    )
                    .encode(
                        x=alt.X(
                            "Item avaliado:N",
                            sort="-y",
                            title="Item avaliado",
                            axis=alt.Axis(labelAngle=-35),
                        ),
                        y=alt.Y(
                            "Nota média:Q",
                            title="Nota média",
                            scale=alt.Scale(domain=[0, 5]),
                        ),
                        color=alt.Color(
                            "Área:N",
                            title="Área",
                            scale=alt.Scale(
                                domain=list(CORES_AREAS.keys()),
                                range=list(CORES_AREAS.values()),
                            ),
                        ),
                        tooltip=[
                            alt.Tooltip("Área:N", title="Área"),
                            alt.Tooltip("Item avaliado:N", title="Item"),
                            alt.Tooltip(
                                "Nota média:Q",
                                title="Nota média",
                                format=".1f",
                            ),
                        ],
                    )
                    .properties(height=460)
                )

                st.altair_chart(
                    grafico_medias,
                    use_container_width=True,
                )

                st.markdown("### Ranking de avaliação")

                ranking_ordenado = ranking.sort_values(
                    "Nota média",
                    ascending=False,
                )

                st.dataframe(
                    ranking_ordenado,
                    use_container_width=True,
                    hide_index=True,
                )

            # NPS
            if "nps_satisfacao_geral" in df.columns:
                st.markdown("### Satisfação geral - escala 0 a 10")

                nps_validos = df["nps_satisfacao_geral"].dropna()

                if not nps_validos.empty:
                    promotores = len(nps_validos[nps_validos >= 9])
                    neutros = len(
                        nps_validos[
                            (nps_validos >= 7)
                            & (nps_validos <= 8)
                        ]
                    )
                    detratores = len(nps_validos[nps_validos <= 6])

                    total_nps = len(nps_validos)

                    nps_score = (
                        ((promotores - detratores) / total_nps) * 100
                        if total_nps > 0
                        else 0
                    )

                    n1, n2, n3, n4 = st.columns(4)

                    with n1:
                        st.metric("Promotores", promotores)

                    with n2:
                        st.metric("Neutros", neutros)

                    with n3:
                        st.metric("Detratores", detratores)

                    with n4:
                        st.metric("NPS", f"{nps_score:.0f}")

                    st.bar_chart(
                        nps_validos.value_counts().sort_index()
                    )

            # SERVIÇOS QUE PRECISAM DE MAIS ATENÇÃO
            if "servico_precisa_atencao" in df.columns:
                st.markdown("### Serviços que precisam de mais atenção")

                atencao = (
                    df["servico_precisa_atencao"]
                    .dropna()
                    .astype(str)
                    .str.split(", ")
                    .explode()
                )

                atencao = atencao[atencao != ""]

                if not atencao.empty:
                    contagem_atencao = (
                        atencao.value_counts()
                        .rename_axis("Área")
                        .reset_index(name="Quantidade")
                    )

                    grafico_atencao = (
                        alt.Chart(contagem_atencao)
                        .mark_bar(
                            cornerRadiusTopLeft=6,
                            cornerRadiusTopRight=6,
                        )
                        .encode(
                            x=alt.X(
                                "Área:N",
                                title="Área",
                                sort="-y",
                            ),
                            y=alt.Y(
                                "Quantidade:Q",
                                title="Quantidade de respostas",
                            ),
                            color=alt.Color(
                                "Área:N",
                                title="Área",
                                scale=alt.Scale(
                                    domain=list(CORES_AREAS.keys()),
                                    range=list(CORES_AREAS.values()),
                                ),
                            ),
                            tooltip=[
                                alt.Tooltip("Área:N", title="Área"),
                                alt.Tooltip(
                                    "Quantidade:Q",
                                    title="Quantidade de respostas",
                                ),
                            ],
                        )
                        .properties(height=400)
                    )

                    st.altair_chart(
                        grafico_atencao,
                        use_container_width=True,
                    )

                else:
                    st.info(
                        "Ainda não há marcações de serviços que precisam de atenção."
                    )

            with st.expander("Ver dados coletados"):
                st.dataframe(df, use_container_width=True)
