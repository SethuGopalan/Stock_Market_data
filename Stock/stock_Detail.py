import dash
from dash import dcc,html,Input,Output,callback,dash_table
import pandas as pd 
# import numpy as np 
import requests


tickers = [
    "AAPL", "MSFT", "GOOGL", "GOOG", "AMZN", "TSLA", "META", "NVDA", "ORCL", "IBM",
    "INTC", "JPM", "BAC", "WFC", "C", "GS", "MS", "XOM", "CVX", "BP", "COP", "RDS.A",
    "RDS.B", "KO", "PEP", "PG", "WMT", "COST", "TGT", "JNJ", "PFE", "MRK", "UNH",
    "AMGN", "T", "VZ", "NFLX", "DIS", "V", "MA", "PYPL", "ADBE", "CRM", "CSCO", "UPS",
    "FDX", "BA", "NKE"
]

time_periods = ["1d", "3mo", "1y"]
data_intervals = ["1d", "1wk", "1mo"]

app=dash.Dash(__name__)



app.layout=html.Div([

    html.H1("Stock Market Application"),

    dcc.Dropdown(id="ticker-id",
    options=[{'label':tick,"value":tick}for tick in tickers],
    value="TSLA"),

    dcc.Dropdown(id="time-id",
    options=[{'label':t,"value":t}for t in time_periods],
    value="1day"),

    dcc.Dropdown(id="intervel-id",
    options=[{'label':t,"value":t}for t in data_intervals],
    value="1day"),

    html.Button('fetch Stock Data',id='stok-id',n_clicks=0),

    html.Div(id="disp-id",children="Select options and click Fetch Stock Data")

])

@app.callback(

    Output("disp-id","children"),
    Input("ticker-id",'value'),
    Input("time-id",'value'),
    Input("intervel-id","value"),
    Input("stok-id","n_clicks")
)

def Stock_extract(ticker_value,time_p_value,intervel_value,n_clicks=0):
    if n_clicks == 0:
        return "please select a valid Ticker ,time and intervel"
    if ticker_value is None or time_p_value is None or intervel_value is None:
        return "plaese provide all the values"
    try:
        response=requests.get('http://Data_Api:5000/stock-data',params={"tickers":ticker_value,'time_period':time_p_value,'data_intervel':intervel_value})

        if response.status_code ==200:
            data=response.json()
            df = pd.DataFrame(data)

            df=df.T
            df.reset_index(inplace=True)
            df.rename(columns={"index": 'Date'},inplace=True)
            return dash_table.DataTable(
                columns=[{"name":i,"id":i}for i in df.columns],
                data=df.to_dict('records'),
                style_table={'overflowX':'auto'},
                style_cell={'textAlign':'center','padding':'5px'}
            )
        else:
            return f"Error fetching data: {response.status_code}"
    except Exception as e:
        return f"Request failed: {str(e)}"

if __name__ == "__main__":

    app.run_server(debug=True)








