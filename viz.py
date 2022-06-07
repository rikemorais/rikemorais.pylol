# Dependencies
from http import server
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from mastery import *


# Structure
app = dash.Dash(__name__)
server = app.server

Level = df["Level"].value_counts().index.sort_values()
Tag = df["Tag"].value_counts().index.sort_values()


# THEME
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])


# Data
df_data = df


# Layout
app.layout = dbc.Container(children=[
            dbc.Row([
                dbc.Col([
                    dbc.Card(
                        [
                            html.H2("PyLol", style={'font-family': 'Voltaire', 'font-size': '60px'}),
                            html.Hr(), 
                            html.P("Dados"),

                            html.H5("Level:", style={"margin-top": "20px"}),
                            dcc.Checklist(df_data["Level"].value_counts().index,
                            df_data["Level"].value_counts().index, id="check_level", 
                            inputStyle={"margin-right": "5px", "margin-left": "20px"}),

                            html.H5("Tag", style={"margin-top": "20px"}),
                            
                            dcc.RadioItems(Tag,
                            "gross income", id="main_variable", 
                            inputStyle={"margin-right": "5px", "margin-left": "20px"}),

                        ], style={"margin": "20px", "padding": "20px", "height": "90vh"})
                    ], md=3),

                dbc.Col([
                    dbc.Row([
                        dbc.Col(dcc.Graph(id="city_fig"), lg=4, sm=12),
                        dbc.Col(dcc.Graph(id="gender_fig"), lg=4, sm=12),
                        dbc.Col(dcc.Graph(id="pay_fig"), lg=4, sm=12)
                    ]),

                    dbc.Row([dcc.Graph(id="income_per_date_fig")]),

                    dbc.Row([dcc.Graph(id="income_per_product_fig")]),

                ], md=9)
            ])

    ], style={"padding": "0px"}, fluid=True)


# Callbacks
# =========  Layout  =========== #
@app.callback([
                Output("city_fig", "figure"),
                Output("gender_fig", "figure"),
                Output("pay_fig", "figure"),
                Output("income_per_date_fig", "figure"),
                Output("income_per_product_fig", "figure"),
            ], 
                [
                    Input("check_level", "value"),
                    Input("main_variable", "value"),
                ])
def render_page_content(Level, main_variable):
    operation = np.count_nonzero if main_variable == "gross income" else np.mean
    df_filtered = df_data[df_data["Level"].isin(Level)]

    df_level = df_filtered.groupby("Level")[main_variable].apply(operation).to_frame().reset_index()
    df_tag = df_filtered.groupby(["Tag", "Level"])[main_variable].apply(operation).to_frame().reset_index()
    df_payment = df_filtered.groupby(["Payment"])[main_variable].apply(operation).to_frame().reset_index()
    df_income_time = df_filtered.groupby("Date")[[main_variable]].apply(operation).reset_index()
    df_product_income = df_filtered.groupby(["Product line", "City"])[[main_variable]].apply(operation).reset_index()

    fig_level = px.bar(df_level, x="Level", y=main_variable)
    fig_gender = px.bar(df_tag, x="Gender", y=main_variable, color="City", barmode='group')
    fig_payment = px.bar(df_payment, y="Payment", x=main_variable, orientation="h")
    fig_income_time = px.bar(df_income_time, y=main_variable, x="Date")
    fig_product_income = px.bar(df_product_income, x=main_variable, y="Product line", color="City", orientation="h")

    for fig in [fig_level, fig_gender, fig_payment, fig_income_time]:
        fig.update_layout(margin=dict(l=0, r=20, t=20, b=20), height=200)
    fig_product_income.update_layout(margin=dict(l=0, r=0, t=20, b=20), height=500, template="minty")
    
    return fig_level, fig_gender, fig_payment, fig_income_time, fig_product_income


# Server
if __name__ == "__main__":
    app.run_server(port=8050, host='0.0.0.0', debug=True)