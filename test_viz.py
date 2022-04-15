import dash
import dash_mantine_components as dmc
import xarray as xr
from dash import html, Input, Output, State, callback, dcc
import dash_bootstrap_components as dbc
import time



"""
app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.CERULEAN],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ]

)
"""

from dash_extensions.enrich import DashProxy, TriggerTransform, MultiplexerTransform, ServersideOutputTransform, NoOutputTransform, BlockingCallbackTransform, LogTransform,DashLogger

app = DashProxy (__name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.CERULEAN],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ],transforms=[
    TriggerTransform(),  # enable use of Trigger objects
    MultiplexerTransform(),  # makes it possible to target an output multiple times in callbacks
    ServersideOutputTransform(),  # enable use of ServersideOutput objects
    NoOutputTransform(),  # enable callbacks without output
    BlockingCallbackTransform(),  # makes it possible to skip callback invocations while a callback is running 
    LogTransform()  # makes it possible to write log messages to a Dash component
])


def project_select():
    component = dmc.Affix([
        dmc.Select(id='project-select',
                   label='Select Project',
                   data=['project1', 'project2']),
    ], position={"top": 60, "right": 20})
    return component


def settings_button():
    component = dmc.Affix([
        dmc.Button('Settings', id='data-viz-settings-drawer-open')
    ], position={"bottom": 20, "left": 20})
    return component

def volume_viz_settings():
    component =    dmc.Group([dbc.Input(placeholder='Low cut: 2Hz'),
                       dbc.Input(placeholder='High cut: 100Hz'),
                       dmc.Switch(
                label="Apply",
                color="blue",
                radius="xl",
                size="sm"
            )
            ], position="left",
                direction="row",
                spacing="md",
                grow=True)
    return component


def settings_drawer():
    component = dmc.Drawer([
        dmc.Accordion(
            [
                dmc.AccordionItem([volume_viz_settings()], label='Volume Viz Settings')
            ]
        )
    ], id='data-viz-menu-drawer',
                           padding="md",
                           position='right',
                           size='40%')
    return component


def iline_volume_select(project):
    component = dmc.Affix([
        dmc.Select(id='iline-volume-select',
                   label='Select Volume',
                   data=[project]),
    ], position={"top": 100, "left": 20})
    return component


def iline_tab():
    component = html.Div([
        dmc.Select(label='Select Volume', id='iline-volume-select', style={"width": 200}),
        html.Br(),
        dmc.Paper([
            html.Div(id='iline-tab-viz', children=[dmc.Skeleton(height=750)]),
        ], radius="sm",
            p="lg",
            shadow="md",
            withBorder=True,),
        html.Br(),
        dcc.Slider(id='iline-slice-select', min=0, max=100, step=10)
    ])
    return component


app.layout = html.Div([
    project_select(),
    settings_drawer(),
    settings_button(),
    dmc.Tabs([
        dmc.Tab([iline_tab()], label='Inline'),
        dmc.Tab([], label='Crossline')
    ],
        color="indigo",
        variant="default",
        tabPadding="sm",
        orientation="horizontal",
        position="left",
        grow=True,),
        dmc.Button("Run", id="btn"),
        html.Br(),
        dmc.Text(id="txt")
])


@callback(
    Output('iline-tab-viz-data', "children"),
    Input('iline-slice-select', "value"),
    prevent_initial_call=True,
)
def handle_iline_volume_select(iline):
    return html.H1(iline)

@callback(
    Output('iline-slice-select', "min"),
    Output('iline-slice-select', "max"),
    Input('iline-volume-select', "value"),
    prevent_initial_call=True,
)
def handle_iline_volume_select(volume):
    if volume == 'project1':
        min, max = 100, 200
    else:
        min, max= 300,400
    return min,max

@callback(
    Output("data-viz-menu-drawer", "opened"),
    Input('data-viz-settings-drawer-open', "n_clicks"),
    prevent_initial_call=True,
)
def handle_project_select(n_clicks):
    return True

@callback(
    Output("iline-volume-select", "data"),
    Input('project-select', "value"),
    prevent_initial_call=True,
)
def handle_open_settings_drawer(project):
    return [project]


@app.callback(Output("txt", "children"), Input("btn", "n_clicks"), log=True)
def do_stuff(n_clicks, logger: DashLogger):
    time.sleep(1)
    logger.info("Here goes some info")
    time.sleep(2)
    logger.warning("This is a warning")
    time.sleep(3)
    logger.error("Some error occurred")
    return f"Run number {n_clicks} completed"


if __name__ == "__main__":
    app.run_server(host="localhost", port=8050, debug=True)
