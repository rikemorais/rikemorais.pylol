from colorama import Style
from dash import Dash, html
import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from database.etl import datadragon


# THEME
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])


# Layout
def generate_table(dataframe, max_rows=200):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns]),
            className="thead-dark"
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ],
        style={"background-color": "#1E1E1E",
               "color": "white",
               "text-align": "center"},
        className="table table-striped table-bordered table-hover"
    )


app.layout = dbc.Container(
    children=[
        dbc.Row([]),
        dbc.Row([
            dbc.Col([generate_table(datadragon())])
        ]),
    ])


# Server
if __name__ == '__main__':
    app.run_server(
        port=8051,
        debug=True)
