import sys, os
sys.path.append(os.path.abspath('.'))

import ds_comp.config as config
import pathlib as pl
from time import strftime, gmtime
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px

# TODO: hover text with competences description and levels
# TODO: button `Save` formatted
# TODO: authentication
# TODO: DNS
# TODO: refresh table with page refresh - state sharing
# TODO: organize work with data

app = dash.Dash(__name__)
server = app.server

APP_PATH = str(pl.Path(__file__).parent.resolve())

personal_competencies = pd.read_csv(os.path.join(APP_PATH, os.path.join("data", "personal_competencies.csv")))

competencies_description = pd.read_csv(os.path.join(APP_PATH, os.path.join("data", "personal_competencies.csv")))

people: list = config.people

filter_name = config.filter_name

app.layout = dcc.Tabs(
                id="tabs", children=[
                dcc.Tab(label='Таблица для заполнения', children=[
                    html.Div(children=[
                    html.Div(
                        className="container",
                        children=[
                            html.Div(
                                className="row",
                                children=[
                                    html.Div(
                                        className='six columns',
                                        children=[html.H3('Матрица компетенций')]),
                                    html.Div(
                                        children=[html.Div(id='status', children='Сохранений нет')]),
                                    html.Div(
                                        className='save-button',
                                        children=[html.Button('Сохранить', id='button-id')])
                                    ]
                            ),
                            html.Div(
                                className="row",
                                children=[
                                    html.Div(
                                        className="twelve columns",
                                        children=[
                                            dash_table.DataTable(
                                                id='table-editable',
                                                columns=(
                                                    [{'id': column, 'name': column}
                                                     for column in personal_competencies.columns]
                                                ),
                                                data=personal_competencies.to_dict('records'),
                                                editable=True
                                            )
                                        ]
                                    )
                                ]
                            ),
                            html.Div(
                                className="row",
                                children=[
                                    html.Div(
                                        className="one-half",
                                        children=[dcc.Graph(id='personal-graphs')]
                                    ),
                                    html.Div(
                                        className="six columns table-results",
                                        children=[
                                            dash_table.DataTable(id='table-results')]
                                    ),
                                ]
                            )
                        ]
                    )
                ]
            )
        ]
    ),
                dcc.Tab(label='Таблица с информацией', children=[
                    html.Div(children=[
                        html.Div(
                            className="container",
                            children=[
                                html.Div(
                                    className="row",
                                    children=[
                                        html.Div(className="twelve columns", children=[
                                            dash_table.DataTable(
                                                id='table-information',
                                                columns=([{'id': column, 'name': column}
                                                          for column in personal_competencies.columns]),
                                                data=personal_competencies.to_dict('records'),
                                                editable=True)])
                                          ]
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ]
        )


# callback to update results and figure
@app.callback(
    [Output("personal-graphs", "figure"), Output('table-editable', 'data')],
    [Input("table-editable", "data_timestamp")],
    [State("table-editable", "data")]
)
def update_output(timestamp, rows):
    global people, filter_name
    df = pd.DataFrame(rows)
    df = df.groupby([filter_name])[people].mean().stack().reset_index().rename(
        columns={'level_1': 'Сотрудник', 0: 'Уровень'})
    figure = px.line_polar(df, r="Уровень", theta="Группа навыков", color="Сотрудник", line_close=True,
        color_discrete_sequence=px.colors.sequential.Plasma[-2::-1], template="plotly_white")
    return figure, rows

@app.callback(
    Output('status', 'children'),
    [Input('button-id', 'n_clicks_timestamp')],
    [State("table-editable", "data")]
)
def update_output_div(n_clicks_timestamp, rows):
    global APP_PATH
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(APP_PATH, os.path.join("data", "personal_competencies.csv")), index=False)
    try:
        updated = 'Последнее сохранение в {}'.format(strftime('%m/%d/%Y %H:%M:%S', gmtime(n_clicks_timestamp/1000.)))
    except TypeError:
        updated = 'Сохранений нет'
    return updated


if __name__ == "__main__":
    app.run_server(debug=True)
