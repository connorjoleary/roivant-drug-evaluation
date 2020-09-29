import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}


df = pd.read_csv('drug_data.csv')

fig = make_subplots(rows=1, cols=2,
    subplot_titles=("Price", "Time to Develop"))

fig.add_trace(
    px.box(df, y="price_annual", hover_data=['name'], points="all", title='Price').data[0],
    row=1, col=1
)

fig.add_trace(
    px.box(df, y="time_to_dev_weeks", hover_data=['name'], points="all").data[0],
    row=1, col=2
)

fig.update_layout(height=700)

@app.callback(
    Output('datatable-row-ids-container', "figure"),
    [Input('datatable-interactivity', "derived_virtual_data"),
     Input('datatable-interactivity', "derived_virtual_selected_rows")])
     
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

    dff = df if rows is None else pd.DataFrame(rows)

    colors = ['#7FDBFF' if i in derived_virtual_selected_rows else '#0074D9'
              for i in range(len(dff))]

    return px.box(df, y="price_annual", hover_name='name', points="all", title='Price', color=colors)

# fig.update_layout(
#     plot_bgcolor=colors['background'],
#     paper_bgcolor=colors['background'],
#     font_color=colors['text']
# )

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Roivant Drug Information',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i, "deletable": False, "selectable": False} for i in df.columns
        ],
        data=df.to_dict('records'),
        editable=False,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        row_selectable="multi",
        row_deletable=False,
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current= 0,
        page_size= 10,
        style_table={
            'overflowY': 'scroll'
        }
    ),
    dcc.Graph(id='datatable-row-ids-container'),

    dcc.Graph(
        id='example-graph-1',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)