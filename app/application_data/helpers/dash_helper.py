from dash import html, dcc, dash_table
from datetime import datetime, date


def render_dashboard_table(data):
    if len(data) > 0:
        columns = data[0].keys()
        cols = []
        for i, k in enumerate(data, 1):
            new_dct = {
                '#': i, 
            }
            for key, value in list(zip(columns, k)):
                new_dct[key] = value 
            cols.append(new_dct)
        table = dash_table.DataTable(
            data=cols,
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(220, 220, 220)',
                }
            ],
            style_header={
                'backgroundColor': 'rgb(30, 30, 30)',
                'color': 'white'
            },
            style_data={
                'backgroundColor': 'rgb(50, 50, 50)',
                'color': 'white',
                'whiteSpace': 'normal',
                'height': 'auto'
            },
            id="test-table"
        )
    else:
        table = dash_table.DataTable(
            data=[
                {"#": 1}
            ],
            id="test-table"
        )
    return table


def render_dashboard_filters(media_sources, companies, platforms, datetime_fmt="%Y-%m-%d %H:%M:%S"):
    if all([media_sources, companies, platforms]):
        return [
            html.Div(
                children=[
                    html.Div(children="Дата начала - дата конца", className="menu-title"),
                    dcc.DatePickerRange(
                        id="date-range",
                        min_date_allowed=date(2019, 1, 1),
                        max_date_allowed=date(2023, 1, 1),
                        start_date=date(2020, 1, 1),
                        end_date=date(2022, 8, 29),
                    ),
                ], className='col-3'
            ),
            
            html.Div(
                children=[
                    html.Div(children="Медиа источник", className="menu-title"),
                    dcc.Dropdown(
                        id="mediasource-filter",
                        options=[
                            {"label": _.name, "value": _.id}
                            for _ in media_sources
                        ],
                        value="",
                        clearable=False,
                        searchable=False,
                        className="dropdown",
                    ),
                ], className='col-3'
            ),
            
            html.Div(
                children=[
                    html.Div(children="Компании", className="menu-title"),
                    dcc.Dropdown(
                        id="company-filter",
                        options=[
                            {"label": _.name, "value": _.id}
                            for _ in companies
                        ],
                        value="",
                        clearable=False,
                        searchable=False,
                        className="dropdown",
                    ),
                ], className='col-3'
            ),
            
            html.Div(
                children=[
                    html.Div(children="Платформа", className="menu-title"),
                    dcc.Dropdown(
                        id="platform-filter",
                        options=[
                            {"label": _.name, "value": _.id}
                            for _ in platforms
                        ],
                        value="",
                        clearable=False,
                        searchable=False,
                        className="dropdown",
                    ),
                ], className='col-3'
            ),
        ]
    else:
        return [
            html.Div(
                children=[
                    html.Div(children="Дата начала - дата конца", className="menu-title"),
                    dcc.DatePickerRange(
                        id="date-range",
                        min_date_allowed=datetime.strptime('2022-01-01 0:0:0', datetime_fmt),
                        max_date_allowed=datetime.now().strftime(datetime_fmt),
                        start_date=datetime.strptime('2022-01-01 0:0:0', datetime_fmt),
                        end_date=datetime.now().strftime(datetime_fmt),
                    ),
                ], className='col-3'
            )
        ]
