#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 17:16:41 2019

@author: michael
"""
#%%
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import plotly 
plotly.tools.set_credentials_file(username='mvfolino68', api_key='')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df2 = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/' +
    '5d1ea79569ed194d432e56108a04d188/raw/' +
    'a9f9e8076b837d541398e999dcbac2b2826a81f8/'+
    'gdp-life-exp-2007.csv')

df = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/'
    'cb5392c35661370d95f300086accea51/raw/'
    '8e0768211f6b747c0db42a9ce9a0937dafcbd8b2/'
    'indicators.csv')

df3=df2[['country','continent']]
df4=df3.drop_duplicates(subset=['country','continent'])

df4 = df4.rename(index=str,columns ={'country':'Country Name'})
df=df.merge(df4,how = 'left', on = 'Country Name')

available_indicators = df['Indicator Name'].unique()

app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='crossfilter-xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Fertility rate, total (births per woman)'
            ),
            dcc.RadioItems(
                id='crossfilter-xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '33%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='crossfilter-yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Life expectancy at birth, total (years)'
            ),
            dcc.RadioItems(
                id='crossfilter-yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ], style={'width': '33%', 'float': 'center', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='crossfilter-zaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='GDP growth (annual %)'
            ),
            dcc.RadioItems(
                id='crossfilter-zaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '33%', 'display': 'inline-block'}),
        
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }),

    html.Div([
        dcc.Graph(
            id='crossfilter-indicator-scatter',
            hoverData={'points': [{'customdata': 'Japan'}]}
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
    html.Div([
        dcc.Graph(id='x-time-series'),
        dcc.Graph(id='y-time-series'),
        dcc.Graph(id='z-time-series'),
    ], style={'display': 'inline-block', 'width': '49%'}),

    html.Div(dcc.Slider(
        id='crossfilter-year--slider',
        min=1962,
#        min=df['Year'].min(),
        max=df['Year'].max(),
        value=df['Year'].max(),
        marks={str(year): str(year) for year in df['Year'].unique()}
    ), style={'width': '49%', 'padding': '0px 20px 20px 20px'})
])


@app.callback(
    dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
    [dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-zaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-type', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-type', 'value'),
     dash.dependencies.Input('crossfilter-zaxis-type', 'value'),
     dash.dependencies.Input('crossfilter-year--slider', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name, zaxis_column_name,
                 xaxis_type, yaxis_type, zaxis_type,                 
                 year_value):
    dff = df[df['Year'] == year_value]
    
    traces = []
    for i in dff.continent.unique():
        dff2 = dff[dff['continent'] == i]
        traces.append(go.Scatter3d(
            x=dff2[dff2['Indicator Name'] == xaxis_column_name]['Value'],
            y=dff2[dff2['Indicator Name'] == yaxis_column_name]['Value'],
            z=dff2[dff2['Indicator Name'] == zaxis_column_name]['Value'],
            text=dff2[dff2['Indicator Name'] == yaxis_column_name]['Country Name'],
            customdata=dff2[dff2['Indicator Name'] == yaxis_column_name]['Country Name'],
            mode='markers',
            opacity=0.9,
            marker={
                'size': 10,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i
        ))
    data = traces

    return {
        'data': data
#            [go.Scatter3d(
#            x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
#            y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
#            z=dff[dff['Indicator Name'] == zaxis_column_name]['Value'],
#            text=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'],
#            customdata=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'],
#            mode='markers',
#            marker={
#                'size': 15,
#                'opacity': 0.5,
#                'line': {'width': 0.5, 'color': 'white'}
#            }
#        )]
        ,
        'layout': go.Layout(
                scene=dict(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            zaxis={
                'title': zaxis_column_name,
                'type': 'linear' if zaxis_type == 'Linear' else 'log'
            }            
            ),
            margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
            height=650,
            hovermode='closest'
        )
    }


def create_time_series(dff, axis_type, title):
    return {
        'data': [go.Scatter(
            x=dff['Year'],
            y=dff['Value'],
            mode='lines+markers'
        )],
        'layout': {
            'height': 225,
            'margin': {'l': 20, 'b': 30, 'r': 10, 't': 10},
            'annotations': [{
                'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
                'xref': 'paper', 'yref': 'paper', 'showarrow': False,
                'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
                'text': title
            }],
            'yaxis': {'type': 'linear' if axis_type == 'Linear' else 'log'},
            'xaxis': {'showgrid': False}
        }
    }


@app.callback(
    dash.dependencies.Output('x-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
     dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-type', 'value')])
def update_y_timeseries(hoverData, xaxis_column_name, axis_type):
    country_name = hoverData['points'][0]['customdata']
    dff = df[df['Country Name'] == country_name]
    dff = dff[dff['Indicator Name'] == xaxis_column_name]
    title = '<b>{}</b><br>{}'.format(country_name, xaxis_column_name)
    return create_time_series(dff, axis_type, title)


@app.callback(
    dash.dependencies.Output('y-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
     dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-type', 'value')])
def update_z_timeseries(hoverData, yaxis_column_name, axis_type):
    dff = df[df['Country Name'] == hoverData['points'][0]['customdata']]
    dff = dff[dff['Indicator Name'] == yaxis_column_name]
    return create_time_series(dff, axis_type, yaxis_column_name)

@app.callback(
    dash.dependencies.Output('z-time-series', 'figure'),
    [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
     dash.dependencies.Input('crossfilter-zaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-zaxis-type', 'value')])
def update_x_timeseries(hoverData, zaxis_column_name, axis_type):
    dff = df[df['Country Name'] == hoverData['points'][0]['customdata']]
    dff = dff[dff['Indicator Name'] == zaxis_column_name]
    return create_time_series(dff, axis_type, zaxis_column_name)

if __name__ == '__main__':
    app.run_server(debug=True)
