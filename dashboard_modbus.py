# ===============================================================
# Arquivo: dashboard_modbus.py
# Autor: Hermes Renato Serra
# Descrição: Dashboard em Dash para exibição de dados Modbus JSON
# ===============================================================

import json
import webbrowser
import os
from dash import Dash, html, dcc
import plotly.graph_objs as go

# Lê os dados do arquivo JSON
with open("dados_modbus.json", encoding="utf-8") as f:
    dados = json.load(f)

# Função para extrair o maior valor (convertendo para float e ignorando valores inválidos)
def max_valor(dados_dict):
    valores = []
    for v in dados_dict.values():
        try:
            valores.append(float(v))
        except (ValueError, TypeError):
            continue
    return max(valores) if valores else 1

# Cria gráfico de barras com margem no topo
def criar_grafico(titulo, dados_dict, unidade):
    max_val = max_valor(dados_dict)
    return dcc.Graph(
        figure=go.Figure(
            data=[
                go.Bar(
                    x=list(dados_dict.keys()),
                    y=[float(v) if v is not None and str(v).replace('.', '', 1).isdigit() else 0 for v in dados_dict.values()],
                    text=[f"{v} {unidade}" if v is not None else "N/A" for v in dados_dict.values()],
                    textposition="auto",
                    marker_color="teal"
                )
            ],
            layout=go.Layout(
                title=titulo,
                yaxis=dict(title=unidade, range=[0, max_val * 1.2])
            )
        )
    )

# Inicialização do app Dash
app = Dash(__name__)
app.title = "Dashboard - Dados Modbus"

# Layout do dashboard
app.layout = html.Div([
    html.H1("Dashboard - Leitura Modbus", style={"textAlign": "center"}),

    html.H2("Temperaturas (°C)"),
    criar_grafico("Temperaturas", dados["temperaturas"], "°C"),

    html.H2("Pressões (bar)"),
    criar_grafico("Pressões", dados["pressoes"], "bar"),

    html.H2("Vazões (L/min)"),
    criar_grafico("Vazões", dados["vazoes"], "L/min"),

    html.H2("Níveis (%)"),
    criar_grafico("Níveis", dados["niveis"], "%"),

    html.H2("Tensões (V)"),
    criar_grafico("Tensões", dados["tensoes"], "V"),

    html.H2("Correntes (A)"),
    criar_grafico("Correntes", dados["correntes"], "A"),
])

# Execução do servidor local
if __name__ == '__main__':
    if os.environ.get("WERKZEUG_RUN_MAIN") != "true":
        webbrowser.open("http://127.0.0.1:8050")
        print("\n✅ Dashboard iniciado com sucesso!")
        print("🌐 Acesse: http://127.0.0.1:8050")
        print("🛑 Para encerrar, pressione Ctrl + C no terminal.\n")

    app.run(debug=True)
