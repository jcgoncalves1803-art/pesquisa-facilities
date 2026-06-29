import streamlit.components.v1 as components
import json


class HighchartsRenderer:

    @staticmethod
    def render_chart(chart_config, height=450):
        html = f"""
        <html>
        <head>
            <script src="https://code.highcharts.com/highcharts.js"></script>
            <script src="https://code.highcharts.com/highcharts-more.js"></script>
            <script src="https://code.highcharts.com/modules/exporting.js"></script>
        </head>
        <body>
            <div id="chart" style="width:100%; height:{height}px;"></div>
            <script>
                Highcharts.chart('chart', {json.dumps(chart_config)});
            </script>
        </body>
        </html>
        """
        components.html(html, height=height + 50)

    @staticmethod
    def radar_fornecedores(dados):
        config = {
            "chart": {"polar": True, "type": "line"},
            "title": {"text": "Comparativo por Servico"},
            "pane": {"size": "85%"},
            "xAxis": {
                "categories": ["Transporte", "Portaria", "Vigilancia", "Limpeza", "Jardinagem", "Refeicao"],
                "tickmarkPlacement": "on",
            },
            "yAxis": {"gridLineInterpolation": "polygon", "min": 0, "max": 5},
            "series": [
                {"name": nome, "data": valores, "pointPlacement": "on"}
                for nome, valores in dados.items()
            ],
        }
        HighchartsRenderer.render_chart(config, height=500)

    @staticmethod
    def ranking_barras(fornecedores, medias):
        colors = ["#4CAF50", "#2196F3", "#FF9800", "#9C27B0", "#E91E63", "#00BCD4"]
        config = {
            "chart": {"type": "bar"},
            "title": {"text": "Ranking de Satisfacao"},
            "xAxis": {"categories": fornecedores},
            "yAxis": {"min": 0, "max": 5, "title": {"text": "Media"}},
            "series": [
                {
                    "name": "Media",
                    "data": [
                        {"y": m, "color": colors[i % 6]}
                        for i, m in enumerate(medias)
                    ],
                    "showInLegend": False,
                }
            ],
            "plotOptions": {
                "bar": {"borderRadius": 5, "dataLabels": {"enabled": True}}
            },
        }
        HighchartsRenderer.render_chart(config)

    @staticmethod
    def distribuicao_pizza(notas_count):
        config = {
            "chart": {"type": "pie"},
            "title": {"text": "Distribuicao de Notas"},
            "plotOptions": {
                "pie": {
                    "innerSize": "50%",
                    "dataLabels": {
                        "enabled": True,
                        "format": "{point.name}: {point.percentage:.1f}%",
                    },
                }
            },
            "series": [
                {
                    "name": "Avaliacoes",
                    "data": [
                        {"name": f"Nota {int(k)}", "y": int(v)}
                        for k, v in sorted(notas_count.items())
                    ],
                }
            ],
        }
        HighchartsRenderer.render_chart(config)
