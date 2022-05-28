from colorama import Style
from dash import Dash, html
import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go

rgapi = open(".token_id").read()
user = "5weCnbUCk3FQ4lFlEKUiut6l6w3i3l5GmHMe3hOt6jacQnw"
api = "https://br1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/"

champions_json = pd.read_json("champions.json")

df = pd.read_json(api+user+"?api_key="+rgapi)

df = df.filter(items=[
    'championId',
    'championLevel',
    'championPoints',
    'championPointsUntilNextLevel',
]
)

df = df.rename(columns={
    'championId': 'ID',
    'championLevel': 'Level',
    'championPoints': 'Points',
    'championPointsUntilNextLevel': 'Next'
}
)

df = df.join(champions_json.set_index("ID"), on="ID", how="left")

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])


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
            dbc.Col([generate_table(df)])
        ]),
    ])


if __name__ == '__main__':
    app.run_server(debug=True)
