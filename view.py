import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import datetime
app = dash.Dash()
server = app.server
scaler = MinMaxScaler(feature_range=(0, 1))
df_nse = pd.read_csv("./data/raw-us-states.csv")
df_nse["Date"] = pd.to_datetime(df_nse.Date, format="%Y-%m-%d")
df_nse.index = df_nse['Date']
data = df_nse.sort_index(ascending=True, axis=0)
new_data = pd.DataFrame(index=range(0, len(df_nse)), columns=['Date', 'Close'])
for i in range(0, len(data)):
    new_data["Date"][i] = data['Date'][i]
    new_data["Close"][i] = data["Close"][i]
new_data.index = new_data.Date
new_data.drop("Date", axis=1, inplace=True)
dataset = new_data.values
train = dataset[0:987, :]
valid = dataset[987:, :]
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(dataset)
x_train, y_train = [], []
for i in range(60, len(train)):
    x_train.append(scaled_data[i - 60:i, 0])
    y_train.append(scaled_data[i, 0])

x_train, y_train = np.array(x_train), np.array(y_train)
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
model = load_model("saved_model.h5")
inputs = new_data[len(new_data) - len(valid) - 60:].values
inputs = inputs.reshape(-1, 1)
inputs = scaler.transform(inputs)
X_test = []
for i in range(60, inputs.shape[0]):
    X_test.append(inputs[i - 60:i, 0])
X_test = np.array(X_test)
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
closing_price = model.predict(X_test)
closing_price = scaler.inverse_transform(closing_price)
train = new_data[:987]
valid = new_data[987:]
valid['Predictions'] = closing_price
df = pd.read_csv("./stock_data.csv")
app.layout = html.Div([

    html.H1("Covid Case Analysis Dashboard", style={"textAlign": "center"}),

    dcc.Tabs(id="tabs", children=[

        dcc.Tab(label='Covid cases ', children=[
            html.Div([
                html.H2("Number of cases", style={"textAlign": "center"}),
                dcc.Graph(
                    id="Actual Data",
                    figure={
                        "data": [
                            go.Scatter(
                                x=train.index,
                                y=valid["Case"],
                                mode='markers'
                            )
                        ],
                        "layout": go.Layout(
                            title='scatter plot',
                            xaxis={'title': 'Date'},
                            yaxis={'title': 'Total cases'}
                        )
                    }
                ),
                html.H2("LSTM Predicted closing price", style={"textAlign": "center"}),
                dcc.Graph(
                    id="Predicted Data",
                    figure={
                        "data": [
                            go.Scatter(
                                x=valid.index,
                                y=valid["Predictions"],
                                mode='markers'
                            )
                        ],
                        "layout": go.Layout(
                            title='scatter plot',
                            xaxis={'title': 'Date'},
                            yaxis={'title': 'Closing Rate'}
                        )
                    }
                )
            ])
        ]),
        dcc.Tab(label='Facebook Stock Data', children=[
            html.Div([
                html.H1("Facebook Stocks High vs Lows",
                        style={'textAlign': 'center'}),

                dcc.Dropdown(id='my-dropdown',  # just added the states need to do the work around it
                             options=[{'State': 'Alabama ', ',': 'Al'},
                                      {'State': 'Alaska ', ',': 'Ak'},
                                      {'State': 'Arizona', ',': 'Az'},
                                      {'State': 'California', ',': 'Ca'},
                                      {'State': 'Arkansas ', 'Cases': 'Ar'},
                                      {'State': 'Colorado  ', 'Cases': 'CO'}
                                      {'State': 'Connecticut ', ',': 'CT'},
                                      {'State': 'Delaware ', ',': 'DE'},
                                      {'State': 'Florida ', ',': 'FL'},
                                      {'State': 'Georgia ', ',': 'GA'},
                                      {'State': 'Hawaii ', ',': 'HI'},
                                      {'State': 'Idaho ', ',': 'ID'},
                                      {'State': 'Illinois ', ',': 'IL'},
                                      {'State': 'Indiana ', ',': 'IN'},
                                      {'State': 'Iowa ', ',': 'IA'},
                                      {'State': 'Louisiana  ', ',': 'LA'},
                                      {'State': 'Maine ', ',': 'ME'},
                                      {'State': 'Maryland ', ',': 'MD'},
                                      {'State': 'Massachusetts ', ',': 'MA'},
                                      {'State': 'Michigan ', ',': 'MI'},
                                      {'State': 'Minnesota ', ',': 'MN'},
                                      {'State': 'Mississippi ', ',': 'MS'},
                                      {'State': 'Missouri ', ',': 'MO'},
                                      {'State': 'Montana ', ',': 'MT'},
                                      {'State': 'Nebraska ', ',': 'NE'},
                                      {'State': 'Nevada ', ',': 'NV'},
                                      {'State': 'New Hampshire', ',': 'NH'},
                                      {'State': 'New Jersey', ',': 'NJ'},
                                      {'State': 'New Mexico', ',': 'NM'},
                                      {'State': 'New York', ',': 'NY'},
                                      {'State': 'North Carolina', ',': 'NC'},
                                      {'State': 'North Dakota', ',': 'ND'},
                                      {'State': 'Ohio ', ',': 'OH'},
                                      {'State': 'Oklahoma ', ',': 'OK'},
                                      {'State': 'Oregon ', ',': 'OR'},
                                      {'State': 'Pennsylvania ', ',': 'PA'},
                                      {'State': 'Rhode Island', ',': 'RI'},
                                      {'State': 'South Carolina', ',': 'SC'},
                                      {'State': 'South Dakota', ',': 'SD'},
                                      {'State': 'Tennessee ', ',': 'TN'},
                                      {'State': 'Texas ', ',': 'TX'},
                                      {'State': 'Utah ', ',': 'UT'},
                                      {'State': 'Vermont ', ',': 'VT'},
                                      {'State': 'Virginia ', ',': 'VA'},
                                      {'State': 'Washington ', ',': 'WA'},
                                      {'State': 'West Virginia', ',': 'WV'},
                                      {'State': 'Wisconsin', ',': 'WI'},
                                      {'State': 'Wyoming ', ',': 'WY'}

                                      ],
                             style={"display": "block", "margin-left": "auto",
                                   "margin-right": "auto", "width": "60%"}),
                dcc.Graph(id='highlow'),




                dcc.Graph(id='volume')
            ], className="container"),
        ])
    ])
])


@app.callback(Output('highlow', 'figure'),
              [Input('my-dropdown', 'value')])
def update_graph(selected_dropdown):
    dropdown= capital_dic={
    'Alabama': 'Montgomery',
    'Alaska': 'Juneau',
    'Arizona':'Phoenix',
    'Arkansas':'Little Rock',
    'California': 'Sacramento',
    'Colorado':'Denver',
    'Connecticut':'Hartford',
    'Delaware':'Dover',
    'Florida': 'Tallahassee',
    'Georgia': 'Atlanta',
    'Hawaii': 'Honolulu',
    'Idaho': 'Boise',
    'Illinios': 'Springfield',
    'Indiana': 'Indianapolis',
    'Iowa': 'Des Monies',
    'Kansas': 'Topeka',
    'Kentucky': 'Frankfort',
    'Louisiana': 'Baton Rouge',
    'Maine': 'Augusta',
    'Maryland': 'Annapolis',
    'Massachusetts': 'Boston',
    'Michigan': 'Lansing',
    'Minnesota': 'St. Paul',
    'Mississippi': 'Jackson',
    'Missouri': 'Jefferson City',
    'Montana': 'Helena',
    'Nebraska': 'Lincoln',
    'Neveda': 'Carson City',
    'New Hampshire': 'Concord',
    'New Jersey': 'Trenton',
    'New Mexico': 'Santa Fe',
    'New York': 'Albany',
    'North Carolina': 'Raleigh',
    'North Dakota': 'Bismarck',
    'Ohio': 'Columbus',
    'Oklahoma': 'Oklahoma City',
    'Oregon': 'Salem',
    'Pennsylvania': 'Harrisburg',
    'Rhoda Island': 'Providence',
    'South Carolina': 'Columbia',
    'South Dakoda': 'Pierre',
    'Tennessee': 'Nashville',
    'Texas': 'Austin',
    'Utah': 'Salt Lake City',
    'Vermont': 'Montpelier',
    'Virginia': 'Richmond',
    'Washington': 'Olympia',
    'West Virginia': 'Charleston',
    'Wisconsin': 'Madison',
    'Wyoming': 'Cheyenne'}           # create a dictionary, key is the state and value is the capital
    #States=list(capital_dic.keys())]
    trace1 = []
    trace2 = []
    for case in selected_dropdown:
        trace1.append(
            go.Scatter(x=df[df["State"] == case]["Date"],
                       y=df[df["State"] == case]["High"],
                       mode='lines', opacity=0.7,
                       name=f'High {dropdown[case]}', textposition='bottom center'))
        trace2.append(
            go.Scatter(x=df[df["State"] == case]["Date"],

                       y=df[df["State"] == case]["Low"],
                       mode='lines', opacity=0.6,
                       name=f'Low {dropdown[case]}', textposition='bottom center'))
    traces = [trace1, trace2]
    data = [val for sublist in traces for val in sublist]
    figure = {'data': data,
              'layout': go.Layout(colorway=["#5E0DAC", '#FF4F00', '#375CB1',
                                            '#FF7400', '#FFF400', '#FF0056'],
                                  height=600,
                                  title=f"High and Low cases for {', '.join(str(dropdown[i]) for i in selected_dropdown)} Over Time",
                                  xaxis={"title": "Date",
                                         'rangeselector': {'buttons': list([{'count': 1, 'label': '1M',
                                                                             'step': 'month',
                                                                             'stepmode': 'backward'},
                                                                            {'count': 6, 'label': '6M',
                                                                             'step': 'month',
                                                                             'stepmode': 'backward'},
                                                                            {'step': 'all'}])},
                                         'rangeslider': {'visible': True}, 'type': 'date'},
                                  yaxis={"title": "Price (USD)"})}
    return figure


@app.callback(Output('volume', 'figure'),
              [Input('my-dropdown2', 'value')])
def update_graph(selected_dropdown_value):
    dropdown = {
    'Alabama': 'Montgomery',
    'Alaska': 'Juneau',
    'Arizona':'Phoenix',
    'Arkansas':'Little Rock',
    'California': 'Sacramento',
    'Colorado':'Denver',
    'Connecticut':'Hartford',
    'Delaware':'Dover',
    'Florida': 'Tallahassee',
    'Georgia': 'Atlanta',
    'Hawaii': 'Honolulu',
    'Idaho': 'Boise',
    'Illinios': 'Springfield',
    'Indiana': 'Indianapolis',
    'Iowa': 'Des Monies',
    'Kansas': 'Topeka',
    'Kentucky': 'Frankfort',
    'Louisiana': 'Baton Rouge',
    'Maine': 'Augusta',
    'Maryland': 'Annapolis',
    'Massachusetts': 'Boston',
    'Michigan': 'Lansing',
    'Minnesota': 'St. Paul',
    'Mississippi': 'Jackson',
    'Missouri': 'Jefferson City',
    'Montana': 'Helena',
    'Nebraska': 'Lincoln',
    'Neveda': 'Carson City',
    'New Hampshire': 'Concord',
    'New Jersey': 'Trenton',
    'New Mexico': 'Santa Fe',
    'New York': 'Albany',
    'North Carolina': 'Raleigh',
    'North Dakota': 'Bismarck',
    'Ohio': 'Columbus',
    'Oklahoma': 'Oklahoma City',
    'Oregon': 'Salem',
    'Pennsylvania': 'Harrisburg',
    'Rhoda Island': 'Providence',
    'South Carolina': 'Columbia',
    'South Dakoda': 'Pierre',
    'Tennessee': 'Nashville',
    'Texas': 'Austin',
    'Utah': 'Salt Lake City',
    'Vermont': 'Montpelier',
    'Virginia': 'Richmond',
    'Washington': 'Olympia',
    'West Virginia': 'Charleston',
    'Wisconsin': 'Madison',
    'Wyoming': 'Cheyenne'  
}
    trace1 = []
    for stock in selected_dropdown_value:
        trace1.append(
            go.Scatter(x=df[df["Case"] == stock]["Date"],
                       y=df[df["Case"] == stock]["Volume"],
                       mode='lines', opacity=0.7,
                       name=f'Volume {dropdown[stock]}', textposition='bottom center'))
    traces = [trace1]
    data = [val for sublist in traces for val in sublist]
    figure = {'data': data,
              'layout': go.Layout(colorway=["#5E0DAC", '#FF4F00', '#375CB1',
                                            '#FF7400', '#FFF400', '#FF0056'],
                                  height=600,
                                  title=f"Case  Volume for {', '.join(str(dropdown[i]) for i in selected_dropdown_value)} Over Time",
                                  xaxis={"title": "Date",
                                         'rangeselector': {'buttons': list([{'count': 1, 'label': '1M',
                                                                             'step': 'month',
                                                                             'stepmode': 'backward'},
                                                                            {'count': 6, 'label': '6M',
                                                                             'step': 'month',
                                                                             'stepmode': 'backward'},
                                                                            {'step': 'all'}])},
                                         'rangeslider': {'visible': True}, 'type': 'date'},
                                  yaxis={"title": "Covid19 Volume"})}
    return figure


if __name__ == '__main__':
    app.run_server(debug=True)
