
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

# app layout
app.layout = html.Div([
    html.H1("Covid Cases Analysis Dashboard", style={"textAlign": "center"}),
    html.Div([
        # dropdown feature to select state
        dcc.Dropdown(id='case-dropdown',
                     options=[
                        # loop through each state
                        {'label': s.stateDict[i], 'value': i}
                        for i in s.stateDict
                     ],
                     value='23',  # default state-Michigan
                     placeholder="Select a state",
                     style={"margin-left": "auto",
                            "margin-right": "auto", "width": "60%"}
                     ),
        dcc.Graph(id='case'),

        html.H1("Covid Deaths Analysis Dashboard",
                style={'textAlign': 'center'}),
        # dropdown feature to select state
        dcc.Dropdown(id='death-dropdown',
                     options=[
                        # loop through each state
                        {'label': s.stateDict[i], 'value': i}
                        for i in s.stateDict
                     ],
                     value='23',  # default state-Michigan
                     placeholder="Select a state",
                     style={"margin-left": "auto",
                            "margin-right": "auto", "width": "60%"}
                     ),
        dcc.Graph(id='death')
    ], className="container"),
])

''' Graph for covid-19 case for selected state '''


@app.callback(Output('case', 'figure'),
              [Input('case-dropdown', 'value')])
def update_graph1(selected_dropdown):
    trace1 = []
    trace2 = []

    # read the state name from state dictionary the read the csv file
    name = s.stateDict[selected_dropdown]
    temp = "./data/" + name + ".csv"
    p_temp = "./predictions/" + name + "_cases.csv"

    # read the actual and predict csv file
    df = pd.read_csv(temp)
    pf = pd.read_csv(p_temp)

    trace1.append(
        go.Scatter(x=df[df["state"] == name]["date"],
                   y=df[df["state"] == name]["cases"],
                   mode='lines', opacity=0.7,
                   name='Actual-Cases', textposition='bottom center')
    )

    trace2.append(
        go.Scatter(x=pf[pf["state"] == name]["date"],
                   y=pf[pf["state"] == name]["cases"],
                   mode='lines', opacity=0.7,
                   name='Predict-Cases', textposition='bottom center')
    )

    traces = [trace1, trace2]
    data = [val for sublist in traces for val in sublist]

    # Graph data set and layout
    figure = {'data': data,
              'layout': go.Layout(
                  colorway=["#5E0DAC", '#FF4F00', '#375CB1',
                            '#FF7400', '#FFF400', '#FF0056'],
                  height=700,
                  title="Covid-19 Cases in " + name,
                  xaxis={"title": "Date", "showgrid": False,
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
                  yaxis={"title": "Total Cases", "showgrid": False})}

    return figure


''' Graph for covid-19 death for selected state'''


@app.callback(Output('death', 'figure'),
              [Input('death-dropdown', 'value')])
def update_graph2(selected_dropdown):
    trace1 = []
    trace2 = []
    # read the state name from state dictionary
    name = s.stateDict[selected_dropdown]
    temp = "./data/" + name + ".csv"
    p_temp = "./predictions/" + name + "_deaths.csv"

    # read the actual and predict csv file
    df = pd.read_csv(temp)
    pf = pd.read_csv(p_temp)

    trace1.append(
        go.Scatter(x=df[df["state"] == name]["date"],
                   y=df[df["state"] == name]["deaths"],
                   mode='lines', opacity=0.7,
                   name='Actual-Deaths', textposition='bottom center'
                   )
    )
    trace2.append(
        go.Scatter(x=pf[pf["state"] == name]["date"],
                   y=pf[pf["state"] == name]["deaths"],
                   mode='lines', opacity=0.7,
                   name='Predict-Deaths', textposition='bottom center'
                   )
    )

    traces = [trace1, trace2]
    data = [val for sublist in traces for val in sublist]

    # Graph data set and layout
    figure = {'data': data,
              'layout': go.Layout(
                  colorway=["#5E0DAC", '#FF4F00', '#375CB1',
                            '#FF7400', '#FFF400', '#FF0056'],
                  height=700,
                  title="Covid-19 Deaths in " + name,
                  xaxis={"title": "Date", "showgrid": False,
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
                  yaxis={"title": "Total Deaths", "showgrid": False})}

    return figure


if __name__ == '__main__':
    app.run_server(debug=True)
