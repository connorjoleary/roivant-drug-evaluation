import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import pandas as pd
import numpy as np

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

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

def direct_drug_profit(years, row, audience=20000):
    print(years)
    num_users = audience*(row['patents_affected_by_drug_percent']/100)*(1-row['patents_developed_inhibitors_percent']/100)
    print(num_users)
    return (num_users)*(row['price_annual']-row['cost_to_create_annual'])*(years-(row['time_to_dev_weeks']/52))

@app.callback(
    Output('profit_projection', "figure"),
    [Input('datatable-interactivity', "derived_virtual_data"),
    Input('datatable-interactivity', "derived_virtual_selected_rows"),
    Input('datatable-interactivity', 'selected_row_ids')])
def update_graphs(rows, derived_virtual_selected_rows, selected_row_ids):
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

    dff = df if rows is None else pd.DataFrame(rows)

    colors = ['#7FDBFF' if i in derived_virtual_selected_rows else '#0074D9'
            for i in range(len(dff))]

    if derived_virtual_selected_rows:
        profit_df = pd.DataFrame()
        profit_df['years'] = range(1,6)
        print(profit_df.years)
        print(dff.iloc[derived_virtual_selected_rows[0]])
        profit_df['profit'] = profit_df.years.apply(direct_drug_profit, row=dff.iloc[derived_virtual_selected_rows[0]])

        return px.line(profit_df, x="years", y="profit", range_y=[-1000000000, 8000000000], title='Expected Direct Profit of Drug '+dff.iloc[derived_virtual_selected_rows[0]]['name'])

    return px.line()

@app.callback(
    Output('datatable-row-ids-container', "figure"),
    [Input('datatable-interactivity', "derived_virtual_data"),
    Input('datatable-interactivity', "derived_virtual_selected_rows"),
    Input('datatable-interactivity', 'selected_columns'),
    Input('datatable-interactivity', 'selected_row_ids')])
def update_graphs(rows, derived_virtual_selected_rows, selected_columns, selected_row_ids):
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

    dff = df if rows is None else pd.DataFrame(rows)

    colors = [dff.iloc[derived_virtual_selected_rows[0]]['name'] if i in derived_virtual_selected_rows else 'All'
            for i in range(len(dff))]

    

    if not selected_columns:
        selected_columns=['price_annual']

    if selected_columns[0].endswith('percent'):
        return px.box(dff, y=selected_columns[0], hover_name='name', points="all", title=selected_columns[0], range_y=[0, 100], color=colors)
        
    if type(dff[selected_columns[0]].iloc[0])==str or type(dff[selected_columns[0]].iloc[0])==np.bool_:
        return px.bar(dff, y=selected_columns[0], hover_name='name', title=selected_columns[0], color=colors, height=700)

    return px.box(dff, y=selected_columns[0], hover_name='name', points="all", title=selected_columns[0], color=colors)

# fig.update_layout(
#     plot_bgcolor=colors['background'],
#     paper_bgcolor=colors['background'],
#     font_color=colors['text']
# )

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Hemophillia A Drug Commercial Success Factors',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i, "deletable": False, "selectable": True} if i != 'name' else {"name": i, "id": i, "deletable": False, "selectable": False} for i in df.columns
        ],
        data=df.to_dict('records'),
        editable=False,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        row_selectable="single",
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current= 0,
        page_size= 10,
    ),
    dcc.Graph(id='datatable-row-ids-container'),
    dcc.Graph(id='profit_projection'),

    # dcc.Graph(
    #     id='example-graph-1',
    #     figure=fig
    # )
])

if __name__ == '__main__':
    app.run_server(debug=True)