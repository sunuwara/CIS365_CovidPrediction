
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import numpy as np
import pandas as pd
import states as s

app = dash.Dash()
server = app.server

app.layout = html.Div([
    html.H1("Covid Cases Analysis Dashboard", style={"textAlign": "center"}),
    html.Div([
        dcc.Dropdown(id='case-dropdown',
                    options=[
                        # loop through each state
                        {'label': s.stateDict[i], 'value': i}
                        for i in s.stateDict
                    ],
                    value='23',
                    placeholder="Select a state",
                    style={"margin-left": "auto", "margin-right": "auto", "width": "60%"}
                    ),
        dcc.Graph(id='case'),

        html.H1("Covid Deaths Analysis Dashboard", style={'textAlign': 'center'}),
        dcc.Dropdown(id='death-dropdown',
                    options=[
                        # loop through each state
                        {'label': s.stateDict[i], 'value': i}
                        for i in s.stateDict
                    ],
                    value='23',
                    placeholder="Select a state",
                    style={"margin-left": "auto", "margin-right": "auto", "width": "60%"}
                    ),
        dcc.Graph(id='death')
    ], className="container"),
])

''' Graph for covid-19 case for selected state'''
@app.callback(Output('case', 'figure'),
              [Input('case-dropdown', 'value')])
def update_graph1(selected_dropdown):
    trace1 = []
    name = s.stateDict[selected_dropdown]
    temp = "./data/" + name + ".csv"
    df = pd.read_csv(temp)

    trace1.append(
        go.Scatter(x=df[df["state"] == name]["date"],
                    y=df[df["state"] == name]["cases"],
                    mode='lines', opacity=0.7,
                    name='Cases ' + name, textposition='bottom center')
    )

    traces = [trace1]
    data = [val for sublist in traces for val in sublist]

    figure = {'data': data,
              'layout': go.Layout(
                  colorway=["#5E0DAC", '#FF4F00', '#375CB1',
                            '#FF7400', '#FFF400', '#FF0056'],
                  height=700,
                  title="Covid-19 Cases in " + name,
                  xaxis={"title": "Date",
                         'rangeselector': {'buttons': list([
                             {'count': 1, 'label': '1D',
                              'step': 'day',
                              'stepmode': 'backward'},
                             {'count': 7, 'label': '7M',
                              'step': 'day',
                              'stepmode': 'backward'},
                             {'count': 14, 'label': '14D',
                              'step': 'day',
                              'stepmode': 'backward'},
                             {'count': 21, 'label': '21D',
                              'step': 'day',
                              'stepmode': 'backward'},
                             {'count': 1, 'label': '1M',
                              'step': 'month',
                              'stepmode': 'backward'},
                             {'count': 6, 'label': '6M',
                              'step': 'month',
                              'stepmode': 'backward'},
                             {'count': 1, 'label': '1Y',
                              'step': 'year',
                              'stepmode': 'backward'},
                             {'step': 'all'}])},
                        },
                  yaxis={"title": "Total Cases"})}

    return figure

''' Graph for covid-19 death for selected state'''
@app.callback(Output('death', 'figure'),
              [Input('death-dropdown', 'value')])
def update_graph2(selected_dropdown):
    trace2 = []
    name = s.stateDict[selected_dropdown]
    temp = "./data/" + name + ".csv"
    df = pd.read_csv(temp)

    trace2.append(
        go.Scatter(x=df[df["state"] == name]["date"],
                    y=df[df["state"] == name]["deaths"],
                    mode='lines', opacity=0.7,
                    name='Deaths ' + name, textposition='bottom center'
                    )
    )
    traces = [trace2]
    data = [val for sublist in traces for val in sublist]

    figure = {'data': data,
              'layout': go.Layout(
                colorway=["#5E0DAC", '#FF4F00', '#375CB1',
                        '#FF7400', '#FFF400', '#FF0056'],
                height=700,
                title="Covid-19 Deaths in " + name,
                xaxis={"title": "Date",
                        'rangeselector': {'buttons': list([
                            {'count': 1, 'label': '1D',
                            'step': 'day',
                            'stepmode': 'backward'},
                            {'count': 7, 'label': '7M',
                            'step': 'day',
                            'stepmode': 'backward'},
                            {'count': 14, 'label': '14D',
                            'step': 'day',
                            'stepmode': 'backward'},
                            {'count': 21, 'label': '21D',
                            'step': 'day',
                            'stepmode': 'backward'},
                            {'count': 1, 'label': '1M',
                            'step': 'month',
                            'stepmode': 'backward'},
                            {'count': 6, 'label': '6M',
                            'step': 'month',
                            'stepmode': 'backward'},
                            {'count': 1, 'label': '1Y',
                            'step': 'year',
                            'stepmode': 'backward'},
                            {'step': 'all'}])},
                    },
                yaxis={"title": "Total Deaths"})}

    return figure


if __name__ == '__main__':
    app.run_server(debug=True, port=2021)

