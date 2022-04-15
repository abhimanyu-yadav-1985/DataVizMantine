import time
import plotly.express as px
import dash_bootstrap_components as dbc
import numpy as np
import dash_mantine_components as dmc
import pandas as pd

from dash import html, dcc, dash_table
from dash_extensions.enrich import Dash, DashProxy, Output, Input, State, Trigger, FileSystemStore,  ServersideOutputTransform, ServersideOutput, callback
from dash_extensions.enrich import ServersideOutputTransform

app = DashProxy (__name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.CERULEAN],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ],
    transforms=[
    ServersideOutputTransform(backend=FileSystemStore(cache_dir="/data/tmp/uploads"))]
    )


app.layout = html.Div(
    [
        dmc.Button("Query data", id="btn-query"),
        dcc.Dropdown(id="dd"),
        html.Div(id='processed-data', children=[]),
        dcc.Loading(dcc.Store(id="store"), fullscreen=True, type="dot"),
    ]
)


@callback(ServersideOutput("store", "data"), Input("btn-query", "n_clicks"))
def query_data(n_clicks):
    time.sleep(10)
    data_df =  pd.read_csv('/data/tmp/000_dummy_project_data.csv')
    return data_df

@callback(Input("store", "data"), Output("dd", "options"))
def query_data_2(df):
    projects = set(list(df['Project']))
    return [{"label": project, "value": project} for project in projects] 
    


@callback(
    Output("processed-data", "children"),
    [Input("dd", "value"),
    State("store", "data")], 
    prevent_initial_call = True
    )
def update_dd(project, df):
    return html.Div([
            dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns]),
            html.Br(),
            html.H1(project)
    ])

if __name__ == "__main__":
    app.run_server(host="localhost", port=8090, debug=True)
    

