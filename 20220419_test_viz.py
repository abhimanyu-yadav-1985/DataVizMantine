from dash_extensions.enrich import DashProxy, TriggerTransform, MultiplexerTransform, ServersideOutputTransform, NoOutputTransform, BlockingCallbackTransform, LogTransform, DashLogger
import dash
import dash_mantine_components as dmc
import xarray as xr
from dash import html, Input, Output, State, callback, dcc
import dash_bootstrap_components as dbc
import time
from dash_iconify import DashIconify

external_stylesheets = [dbc.themes.CERULEAN]

app = DashProxy(__name__,
                suppress_callback_exceptions=True,
                external_stylesheets=external_stylesheets,
                meta_tags=[
                    {"name": "viewport", "content": "width=device-width, initial-scale=1"}
                ], transforms=[
                    TriggerTransform(),  # enable use of Trigger objects
                    # makes it possible to target an output multiple times in callbacks
                    MultiplexerTransform(),
                    ServersideOutputTransform(),  # enable use of ServersideOutput objects
                    NoOutputTransform(),  # enable callbacks without output
                    # makes it possible to skip callback invocations while a callback is running
                    BlockingCallbackTransform(),
                    LogTransform()  # makes it possible to write log messages to a Dash component
                ])

# -----------------------
# Utility Functions
# -----------------------


def get_projects_for_user(user_id):
    return ['project1', 'project2']


def get_volume_datasets_for_project(project_id):
    if project_id is None:
        return []
    else:
        return [project_id]


def get_dataset_metadata(dataset_id):
    pass


def get_data_arrays_in_dataset(dataset_id):
    pass


def get_data_array_metadata(dataset_id, data_array_name):
    pass


def get_data_slice(dataset_id, data_array_id, slice_dim, slice_val):
    pass


def apply_bandpass_filter(low_cut, high_cut):
    pass


def interpolate_slice(x, y, z, x_new, y_new):
    pass


def rasterize_slice(z, height, width):
    pass


def get_available_color_maps():
    return [
        {"value": "react", "label": "React"},
        {"value": "ng", "label": "Angular"},
        {"value": "svelte", "label": "Svelte"},
        {"value": "vue", "label": "Vue"},
    ]

# -----------------------
# Settings Drawer
# -----------------------


def volume_filter():
    component = dmc.Group([dbc.Input(placeholder='Low cut: 2Hz'),
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


def volume_color_scale():
    component = dcc.Slider(id='color-temperature-select', min=0, max=100, step=1,  marks=None,
                           tooltip={"placement": "bottom", "always_visible": True})
    return component


def volume_color_map():
    component = dmc.Chips(
        data=get_available_color_maps(),
        color="blue",
        radius="xl",
        size="sm",
        spacing="xs",
        variant="filled",
        multiple=False,
    )
    return component


def volume_color_settings():
    component = dmc.Group([
        dmc.Text("Color Temperature", size="lg", color='blue'),
        volume_color_scale(),
        dmc.Text("Color Map", size="lg", color='blue'),
        volume_color_map()
    ],
        position="left",
        direction="column",
        spacing="md",
        grow=True
    )
    return component


def volume_viz_settings():
    component = dmc.Group([
        volume_filter(),
        dmc.Divider(variant="solid"),
        volume_color_settings()
    ],
        position="left",
        direction="column",
        spacing="md",
        grow=True
    )
    return component


def settings_drawer():
    component = dmc.Drawer([
        dmc.Accordion(
            [
                dmc.AccordionItem([volume_viz_settings()],
                                  label='Volume')
            ]
        )
    ], id='data-viz-menu-drawer',
        title='Visualization Settings',
        padding="md",
        position='right',
        size='40%')
    return component

# -----------------------
# Inline Tab
# -----------------------





def select_iline_dataset():
    component = html.Div([
        dmc.Select(label='Select DataSet',
                   id='iline-dataset-select', style={"width": 300},
                   persistence=True, persistence_type='session',
                   icon=[DashIconify(icon="bxs:data")]),
        dmc.Affix(dmc.Button(
            " Dataset Info",
            id = 'iline-dataset-info-modal-button',
            variant="filled",
            color="blue",
            radius="sm",
            size="xs",
            compact=True,
            loading=False,
        ), position={"top": 50, "left": 235})
    ])

    return component


def select_iline_data_array():
    component = html.Div([
        dmc.Select(label='Select DataArray',
                   id='iline-data-array-select', style={"width": 300},
                   persistence=True, persistence_type='session',
                   icon=[DashIconify(icon="carbon:data-vis-4")]),
        dmc.Affix(dmc.Button(
            " DataArray Info",
            id = 'iline-data-array-info-modal-button',
            variant="filled",
            color="blue",
            radius="sm",
            size="xs",
            compact=True,
            loading=False,
        ), position={"top": 50, "left": 535})
    ])
    return component


def iline_data_select():
    component = dmc.Group([
        select_iline_dataset(),
        select_iline_data_array()
    ], position="left",
        direction="row",
        spacing="md", align='center')
    return component


def iline_tab():
    component = dmc.Container([
        iline_data_select(),
        html.Br(),
        dmc.Paper([
            html.Div(id='iline-tab-viz', children=[dmc.Skeleton(height=650)]),
        ], radius="sm",
            p="lg",
            shadow="md",
            withBorder=True,),
        html.Br(),
        dcc.Slider(id='iline-slice-select', min=0, max=100, step=10,  marks=None,
                   tooltip={"placement": "bottom", "always_visible": True})
    ], fluid=True)
    return component

# -----------------------
# Page layout
# -----------------------



def iline_dataset_info_modal():
    component = html.Div([dmc.Modal(
        id = 'iline-dataset-info-modal',
        title="Dataset Info",
        size="55%",
        centered=True,
        children=[dmc.Text("Information about the selected dataset")]),])
    return component


def project_info_modal():
    component = html.Div([dmc.Modal(
        id = 'project-info-modal',
        title="Project Info",
        size="55%",
        centered=True,
        children=[dmc.Text("Information about the selected Project")]),])
    return component


def iline_data_array_info_modal():
    component = html.Div([dmc.Modal(
        id = 'iline-data-array-info-modal',
        title="DataArray Info",
        size="55%",
        centered=True,
        children=[dmc.Text("Information about the selected DataArray")]),])
    return component

def project_select():
    component = html.Div([dmc.Affix([
        dmc.Select(id='project-select',
                   label='Select Project',
                   data=get_projects_for_user(user_id=1),
                   style={"width": 300},
                   persistence=True,
                   persistence_type='session',  icon=[DashIconify(icon="octicon:project-24")]),
    ], position={"top": 50, "right": 20}),
        dmc.Affix(dmc.Button(
            "Project Info",
            id='project-info-modal-button',
            variant="filled",
            color="blue",
            radius="sm",
            size="xs",
            compact=True,
            loading=False,
        ), position={"top": 50, "right": 20})

    ])
    return component


def settings_button():
    component = dmc.Affix([
        dmc.Button('Settings', id='data-viz-settings-drawer-open')
    ], position={"bottom": 30, "left": 20})
    return component


app.layout = html.Div([
    project_select(),
    settings_drawer(),
    settings_button(),
    iline_dataset_info_modal(),
    iline_data_array_info_modal(),
    project_info_modal(),
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
])


# -----------------------
# CALL BACKS
# -----------------------

@callback(
    Output('iline-slice-select', "min"),
    Output('iline-slice-select', "max"),
    Input('iline-dataset-select', "value"),
    prevent_initial_call=True,
)
def handle_iline_volume_select(volume):
    if volume == 'project1':
        min, max = 100, 200
    else:
        min, max = 300, 400
    return min, max


@callback(
    Output("iline-dataset-select", "data"),
    Input('project-select', "value"),
)
def handle_project_select(project_id):
    project_datasets_for_select = get_volume_datasets_for_project(project_id)
    return project_datasets_for_select


@callback(
    Output("data-viz-menu-drawer", "opened"),
    Input('data-viz-settings-drawer-open', "n_clicks"),
    prevent_initial_call=True,
)
def handle_open_settings_drawer(n_clicks):
    return True


@app.callback(
    Output("iline-dataset-info-modal", "opened"),
    Input("iline-dataset-info-modal-button", "n_clicks"),
    State("iline-dataset-info-modal", "opened"),
    prevent_initial_call=True,
)
def handle_iline_dataset_info_toggle_modal(n_clicks, opened):
    return not opened

@app.callback(
    Output("project-info-modal", "opened"),
    Input("project-info-modal-button", "n_clicks"),
    State("project-info-modal", "opened"),
    prevent_initial_call=True,
)
def handle_project_info_toggle_modal(n_clicks, opened):
    return not opened


@app.callback(
    Output("iline-data-array-info-modal", "opened"),
    Input("iline-data-array-info-modal-button", "n_clicks"),
    State("iline-data-array-info-modal", "opened"),
    prevent_initial_call=True,
)
def handle_iline_data_array_info_toggle_modal(n_clicks, opened):
    return not opened

if __name__ == "__main__":
    app.run_server(host="localhost", port=8050, debug=True)
