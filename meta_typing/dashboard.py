# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
import duckdb
import dash
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table

#df = pd.read_csv('https://raw.githubusercontent.com/JonathanWamsley/pokemon_cards_project/master/data/snapshot_2020-03-24.csv')
def connect_db():
    con = duckdb.connect(database='words.db', read_only=False)
    return con

def query_word_recommendation(query):
    list_type, metric, amount = query = query
    con = connect_db()
    df = con.execute(f'''
    SELECT word, AVG({metric}::DOUBLE)
    from word_stats
    WHERE word_list = {list_type} AND capital = 'false' AND symbols = 'false'
    GROUP BY word ORDER BY AVG({metric}::DOUBLE) 
    LIMIT {amount}
    ''').fetchdf()
    con.close()
    return df

def query_word_by_date(word):
    con = connect_db()
    df = con.execute(f"""
    SELECT avg(wpm) as wpm, date
    from word_stats
    where word = '{word}'
    group by date
    ORDER BY date
    """).fetchdf()
    con.close()
    return df

def query_word_list_by_date(list_type):
    con = connect_db()
    df = con.execute(f'''
    SELECT avg(wpm) as wpm, date
    from word_stats
    where word_list = {list_type}
    group by date
    ORDER BY date
    ''').fetchdf()
    con.close()
    return df

def query_word_list_all_by_date():
    con = connect_db()
    df = con.execute(f'''
    SELECT avg(wpm) as wpm, date
    from word_stats
    group by date
    ORDER BY date
    ''').fetchdf()
    con.close()
    return df

def query_by_word_list(list_type):
    con = connect_db()
    df = con.execute(f'''
    SELECT word, round(AVG(wpm::DOUBLE),2) as wpm, round(AVG(wpm_space::DOUBLE),2) as wpm_space, round(100*AVG(accuracy::DOUBLE),2) as accuracy
    FROM word_stats
    where word_list = {list_type}
    GROUP BY word ORDER BY AVG(wpm_space::DOUBLE) DESC
    ''').fetchdf()
    con.close()
    return df

def query_by_word_list_all(list_type):
    con = connect_db()
    df = con.execute(f'''
    SELECT word, round(AVG(wpm::DOUBLE),2) as wpm, round(AVG(wpm_space::DOUBLE),2) as wpm_space, round(100*AVG(accuracy::DOUBLE),2) as accuracy
    FROM word_stats
    where word_list = {list_type}
    GROUP BY word ORDER BY AVG(wpm_space::DOUBLE) DESC
    ''').fetchdf()
    con.close()
    return df

def query_all():
    con = connect_db()
    df = con.execute(f'''
    SELECT word, word_list, round(AVG(wpm::DOUBLE),2) as wpm, round(AVG(wpm_space::DOUBLE),2) as wpm_space, round(100*AVG(accuracy::DOUBLE),2) as accuracy
    FROM word_stats
    GROUP BY word, word_list ORDER BY AVG(wpm_space::DOUBLE) DESC
    ''').fetchdf()
    con.close()
    return df

df = query_all()



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

PAGE_SIZE = 5

app.layout = html.Div(children=[
    html.H1(
        children='MetaTyping Dashboard',
        style={'textAlign': 'center'},
    ),
    html.Div([
        html.Div(id='word_graph_list_container', className='six columns'),
        html.Div(id='word_graph_container',className='six columns'),
        
    ],className='row'),

    
    html.Div([
        html.Div([
            dcc.Dropdown(id='word_list_dropdown',
            style={'textAlign': 'center'},
                options=[
                        {'label': 'top 100', 'value': '1'},
                        {'label': 'top 300', 'value': '2'},
                        {'label': 'top 600', 'value': '3'},
                        {'label': 'top 1000', 'value': '4'},
                        {'label': 'top 3000', 'value': '5'},
                        {'label': 'top 10000', 'value': '6'},
                        {'label': 'All', 'value': 'all'},
                ],
                value='1',
                multi=False,
                clearable=False
            ),
        ],className='six columns'),

        html.Div([
            dcc.Input(id='word_input', value='word', type='text',
            style={'textAlign': 'center'},
            ),
        ], style={'text-align': 'center'}),

    ],className='row'),

    html.Div([
        html.Div(
            dash_table.DataTable(
                id='table-paging-with-graph',
                columns=[
                    {"name": i, "id": i} for i in ['word', 'wpm', 'wpm_space', 'accuracy']
                ],
                page_current=0,
                page_size=20,
                page_action='custom',

                filter_action='custom',
                filter_query='',

                sort_action='custom',
                sort_mode='multi',
                sort_by=[],
            ),
            style={'height': 750, 'overflowY': 'scroll'},
            className='six columns'
        ),
        html.Div(
            id='table-paging-with-graph-container',
            className="five columns"
        )
    ], className="row")
    
])

operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']]


def split_filter_part(filter_part):
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part

                return name, operator_type[0].strip(), value

    return [None] * 3


@app.callback(
    Output('table-paging-with-graph', "data"),
    [Input('table-paging-with-graph', "page_current"),
     Input('table-paging-with-graph', "page_size"),
     Input('table-paging-with-graph', "sort_by"),
     Input('table-paging-with-graph', "filter_query"),
     Input('word_list_dropdown', 'value')])
def update_table(page_current, page_size, sort_by, filter, word_list_value):
    filtering_expressions = filter.split(' && ')
    dff = df
    for filter_part in filtering_expressions:
        col_name, operator, filter_value = split_filter_part(filter_part)

        if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
            # these operators match pandas series operator method names
            dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
        elif operator == 'contains':
            dff = dff.loc[dff[col_name].str.contains(filter_value)]
        elif operator == 'datestartswith':
            # this is a simplification of the front-end filtering logic,
            # only works with complete fields in standard format
            dff = dff.loc[dff[col_name].str.startswith(filter_value)]

    if len(sort_by):
        dff = dff.sort_values(
            [col['column_id'] for col in sort_by],
            ascending=[
                col['direction'] == 'asc'
                for col in sort_by
            ],
            inplace=False
        )
    if word_list_value == 'all':
        pass
    else:
        dff = dff.loc[dff['word_list'] == int(word_list_value)]

    return dff.iloc[ 
        page_current*page_size: (page_current + 1)*page_size
    ].to_dict('records')


@app.callback(
    Output('table-paging-with-graph-container', "children"),
    [Input('table-paging-with-graph', "data")])
def update_graph(rows):
    dff = pd.DataFrame(rows)
    return html.Div(
        [
            dcc.Graph(
                id=column,
                figure={
                    "data": [
                        {
                            "x": dff["word"],
                            "y": dff[column] if column in dff else [],
                            "type": "bar",
                            "marker": {"color": "#0074D9"},
                        }
                    ],
                    "layout": {
                        'title':f'{column}',
                        "xaxis": {"automargin": True},
                        "yaxis": {'title': f"{column}", "automargin": True},
                        "height": 250,
                        "margin": {"t": 50, "l": 50, "r": 0},
                    },
                },
            )
            for column in ["wpm", "wpm_space", "accuracy"]
        ]
    )

@app.callback(
    [
        Output('word_graph_list_container', "children"),
    ],
    [
        Input('word_list_dropdown', 'value')
    ])
def update_word_listgraph(word_list_value):
    if word_list_value == 'all':
        df_by_word_list = query_word_list_all_by_date()
    else:
        df_by_word_list = query_word_list_by_date(word_list_value)
        
    word_list_mapping = {
        '1': 'top 100',
        '2': 'top 300',
        '3': 'top 600',
        '4': 'top 1000',
        '5': 'top 3000',
        '6': 'top 10000',
        'all': 'All',
    }
    word_list_graph = [dcc.Graph(id='word_list_graph',
                    figure = {
                        'data': [
                                {
                                'x':df_by_word_list.date,
                                'y':df_by_word_list.wpm,
                                'type':'line',
                                'name': word_list_value
                                },
                            ],
                        'layout': {
                            'title': f"Average wpm for {word_list_mapping[word_list_value]}",
                            'xaxis': {'title': f"date"},
                            'yaxis': {'title': f"wpm"},
                        },
                    }),
    ]
    return word_list_graph

@app.callback(
    [
        Output('word_graph_container', 'children'),
    ],
    [
        Input('word_input', 'value'),
    ]
)
def update_word_data(word_value):
    df_by_word = query_word_by_date(word_value)
    word_graph = [
        dcc.Graph(id='word_graph',
            figure = {
                'data': [
                    {'x':df_by_word.date, 'y': df_by_word.wpm, 'type':'line', 'name': word_value},
                    ],
                'layout': {
                    'title': f"Average wpm date for '{word_value}'",
                    'xaxis': {'title': f"date"},
                    'yaxis': {'title': f"wpm"},
                },
            })
    ]
    return word_graph


if __name__ == '__main__':
    app.run_server(debug=True)
