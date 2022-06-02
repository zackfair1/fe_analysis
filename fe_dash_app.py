"""
This code aims to an interactive plotly/dash dashboard to analyze the tweets targeting the flat earth theory between 2010 and 2022.
"""

from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px
import time

# Dataframe
url='https://drive.google.com/file/d/1oq_J-r9psIY8xPwsY2u2Hal_NF21ATec/view?usp=sharing'
url='https://drive.google.com/uc?id=' + url.split('/')[-2]
df = pd.read_csv(url)
df['year'] = pd.to_datetime(df.date).dt.year
df['datetime'] = pd.to_datetime(df.date).dt.date
df2 = pd.read_csv(
    'https://raw.githubusercontent.com/zackfair1/fe_analysis/main/data_by_year.csv')


# Stylesheet (from the Dash templates)
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Main app
app = Dash(__name__, external_stylesheets=external_stylesheets)

# For Heroku deployment
server = app.server

app.layout = html.Div([
    html.Div([
        html.H3('Twitter - The Flat Earth theory discovery'),
        html.A('Github Repo',href='https://github.com/zackfair1/fe_analysis', target="_blank")
    ], style={'width':'90%', 'margin':'5px'}),
    html.Div([
            dcc.Graph(id='graph1', style={'border':'1px black solid', 'margin':'10px 0','width':'100%'}),
            html.Div([
                dcc.RangeSlider(df.year.min(), df.year.max(), 1, value=[2015, 2017], id='my-range-slider',marks={i:str(i) for i in df.year.sort_values(ascending=True).unique().tolist()}),
            ], style={'margin':'10px','width':'100%','background':'white','border':'0.5px black solid','padding':'10px'}),
            dcc.Graph(id='graph2', style={'border':'1px black solid', 'margin':'10px 0','width':'100%'}),
            html.Div([
                # dcc.RangeSlider(df.n_like.min(), df.n_like.max(), value=[10, 25000], id='n_likes_slider'),
                dcc.Input(id="input_range_1",type="number", placeholder="0", min=0, value=0, debounce=True),
                dcc.Loading(
                    id="loading-1",
                    type="default",
                    children=html.Div(id="loading-output-1"),
                    style={'margin':'25px'}
                ),
                dcc.Input(id="input_range_2", type="number",placeholder="25000", min=0, value=25000, debounce=True),
                dcc.Loading(
                    id="loading-2",
                    type="default",
                    children=html.Div(id="loading-output-2"),
                    style={'margin':'25px'}
                ),
            ], style={'margin':'10px','width':'60%','background':'white','border':'0.5px black solid','padding':'10px'}),
    ], style={'width':'90%', 'margin':'5px', 'display':'flex','justify-content':'center','flex-wrap':'wrap'}),
], style={'display':'flex','justify-content':'center','flex-wrap':'wrap', 'width':'97vw', 'text-align':'center'})

@app.callback(
    Output('graph1', 'figure'),
    Output('graph2', 'figure'),
    [Input('my-range-slider', 'value'),
     Input('input_range_1', 'value'),
     Input('input_range_2', 'value')])
def update_output(value, value2, value3):
    df4 = df2[df2.year.between(value[0], value[1])]
    fig1 = px.area(df4, x='datetime', y='count', template='simple_white', hover_name='datetime',
                   hover_data={'count': True, 'month': True, 'datetime': False})
    fig1.update_layout(title={ 'text': f'<b>Number of Flat Earth tweets between {df4.datetime.iloc[0]} and {df4.datetime.iloc[-1]}</b><br>',
        'y': 0.94,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {'size': 20}
        })
    df3 = df[df.year.between(value[0], value[1])]
    df3 = df3[df3['n_like'].between(value2, value3)]
    fig2 = px.area(df3, x='datetime', y='n_like', template='simple_white', hover_name='date',
              hover_data={'n_like': True,'date':False, 'content':True,'id':False,'datetime':False},)
    fig2.update_layout(title={ 'text': f'<b>Flat Earth tweets between {df3.datetime.iloc[-1]} and {df3.datetime.iloc[0]} - <br>Threshold of {df3.n_like.min()} and {df3.n_like.max()} likes</b><br>',
        'y': 0.94,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {'size': 20}
        })
    return fig1, fig2

@app.callback(Output("loading-output-1", "value"),
              Output("loading-output-2","value"),
              [Input("input_range_1", "value"),
               Input("input_range_2", "value"),]
              )
def input_triggers_spinner(value, value1):
    if value < 0:
        value = 0
    if value > value1:
        value1 = value+1
    if value1 > df.n_like.max():
        value1 = df.n_like.max()
    time.sleep(1.5)
    return value, value1

if __name__ == '__main__':
    app.run_server(debug=False)
    
    