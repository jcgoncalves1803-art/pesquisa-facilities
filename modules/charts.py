import streamlit.components.v1 as components
import json


class HighchartsRenderer:

    HIGHCHARTS_CDN = """
    <script src="https://code.highcharts.com/highcharts.js"></script>
    <script src="https://code.highcharts.com/highcharts-more.js"></script>
    <script src="https://code.highcharts.com/modules/exporting.js"></script>
    <script src="https://code.highcharts.com/modules/export-data.js"></script>
    <script src="https://code.highcharts.com/modules/accessibility.js"></script>
    <script src="https://code.highcharts.com/modules/solid-gauge.js"></script>
    <script src="https://code.highcharts.com/modules/wordcloud.js"></script>
    <script src="https://code.highcharts.com/modules/heatmap.js"></script>
    <script src="https://code.highcharts.com/modules/drilldown.js"></script>
    """

    @staticmethod
    def render_chart(config, height=450):
        html = f"""
        <html>
        <head>{HighchartsRenderer.HIGHCHARTS_CDN}</head>
        <body>
            <div id="chart" style="width:100%; height:{height}px;"></div>
            <script>
                Highcharts.chart('chart', {json.dumps(config)});
            </script>
        </body>
        </html>
        """
        components.html(html, height=height + 50)

    @staticmethod
    def gauge_nps(valor):
        config = {
            "chart": {
                "type": "gauge",
                "plotBackgroundColor": None,
                "plotBorderWidth": 0,
                "plotShadow": False,
                "height": "80%"
            },
            "title": {"text": "NPS - Satisfacao Geral"},
            "pane": {
                "startAngle": -90,
                "endAngle": 89.9,
                "background": None,
                "center": ["50%", "75%"],
                "size": "110%"
            },
            "yAxis": {
                "min": 0,
                "max": 10,
                "tickPixelInterval": 72,
                "tickPosition": "inside",
                "tickLength": 20,
                "tickWidth": 2,
                "labels": {"distance": 20, "style": {"fontSize": "14px"}},
                "plotBands": [
                    {"from": 0, "to": 6, "color": "#DF5353", "thickness": 20},
                    {"from": 6, "to": 8, "color": "#DDDF0D", "thickness": 20},
                    {"from": 8, "to": 10, "color": "#55BF3B", "thickness": 20}
                ]
            },
            "series": [{
                "name": "NPS",
                "data": [round(valor, 1)],
                "dataLabels": {
                    "format": "{y}/10",
                    "borderWidth": 0,
                    "style": {"fontSize": "24px"}
                },
                "dial": {"radius": "80%", "backgroundColor": "gray"},
                "pivot": {"backgroundColor": "gray", "radius": 6}
            }]
        }
        HighchartsRenderer.render_chart(config, height=350)

    @staticmethod
    def column_drilldown(categorias, valores):
        series_data = [{"name": cat, "y": val} for cat, val in zip(categorias, valores)]
        config = {
            "chart": {"type": "column"},
            "title": {"text": "Satisfacao por Servico"},
            "subtitle": {"text": "Media de cada servico"},
            "xAxis": {"type": "category"},
            "yAxis": {"min": 0, "max": 5, "title": {"text": "Nota Media"}},
            "legend": {"enabled": False},
            "plotOptions": {
                "series": {
                    "borderWidth": 0,
                    "dataLabels": {"enabled": True, "format": "{point.y:.1f}"},
                    "colorByPoint": True
                }
            },
            "series": [{"name": "Servicos", "data": series_data}]
        }
        HighchartsRenderer.render_chart(config)

    @staticmethod
    def stacked_bar(categorias, dados):
        series = []
        cores = {
            5: "#27ae60", 4: "#2ecc71", 3: "#f39c12",
            2: "#e67e22", 1: "#e74c3c"
        }
        nomes = {
            5: "Muito satisfeito (5)", 4: "Satisfeito (4)",
            3: "Neutro (3)", 2: "Insatisfeito (2)",
            1: "Muito insatisfeito (1)"
        }
        for nota in [5, 4, 3, 2, 1]:
            if nota in dados:
                series.append({
                    "name": nomes[nota],
                    "data": dados[nota],
                    "color": cores[nota]
                })
        config = {
            "chart": {"type": "bar"},
            "title": {"text": "Distribuicao de Notas por Servico"},
            "xAxis": {"categories": categorias},
            "yAxis": {"min": 0, "title": {"text": "Quantidade"}, "stackLabels": {"enabled": True}},
            "legend": {"reversed": True},
            "plotOptions": {"series": {"stacking": "normal"}},
            "series": series
        }
        HighchartsRenderer.render_chart(config)

    @staticmethod
    def spider_web(categorias, medias):
        config = {
            "chart": {"polar": True, "type": "line"},
            "title": {"text": "Radar de Satisfacao"},
            "pane": {"size": "80%"},
            "xAxis": {
                "categories": categorias,
                "tickmarkPlacement": "on",
                "lineWidth": 0
            },
            "yAxis": {
                "gridLineInterpolation": "polygon",
                "lineWidth": 0,
                "min": 0,
                "max": 5
            },
            "series": [{"name": "Media", "data": medias, "pointPlacement": "on"}]
        }
        HighchartsRenderer.render_chart(config, height=500)

    @staticmethod
    def wordcloud(palavras):
        data = [{"name": palavra, "weight": freq} for palavra, freq in palavras.items()]
        config = {
            "series": [{
                "type": "wordcloud",
                "data": data,
                "name": "Frequencia"
            }],
            "title": {"text": "Palavras Mais Citadas"}
        }
        HighchartsRenderer.render_chart(config)

    @staticmethod
    def pie_detalhado(dados):
        config = {
            "chart": {"type": "pie"},
            "title": {"text": "Distribuicao de Respostas"},
            "tooltip": {"pointFormat": "{series.name}: <b>{point.percentage:.1f}%</b>"},
            "plotOptions": {
                "pie": {
                    "allowPointSelect": True,
                    "cursor": "pointer",
                    "dataLabels": {"enabled": True, "format": "<b>{point.name}</b>: {point.percentage:.1f}%"},
                    "showInLegend": True
                }
            },
            "series": [{"name": "Respostas", "colorByPoint": True, "data": dados}]
        }
        HighchartsRenderer.render_chart(config)

    @staticmethod
    def ranking_barras(fornecedores, medias):
        colors = ["#4CAF50", "#2196F3", "#FF9800", "#9C27B0", "#E91E63", "#00BCD4"]
        config = {
            "chart": {"type": "bar"},
            "title": {"text": "Ranking de Satisfacao"},
            "xAxis": {"categories": fornecedores},
            "yAxis": {"min": 0, "max": 5, "title": {"text": "Media"}},
            "series": [{
                "name": "Media",
                "data": [{"y": m, "color": colors[i % 6]} for i, m in enumerate(medias)],
                "showInLegend": False,
            }],
            "plotOptions": {"bar": {"borderRadius": 5, "dataLabels": {"enabled": True}}}
        }
        HighchartsRenderer.render_chart(config)
