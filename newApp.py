import streamlit as st 
from datetime import date 
#from fbprophet import Prophet
#from fbprophet.plot import plot_plotly 
import calendar


import numpy as np 
import datetime 
import pandas as pd 
import requests
import json 
import matplotlib.pyplot as plt 
from calendar import day_name

from plotly import graph_objs as go 


def plot_tasi(tasi):
     fig = go.Figure()
     fig.add_trace(go.Scatter(x = tasi['date'],
                              y = tasi['open'],
                              name='open'
                              )
                    )

     fig.add_trace(go.Scatter(x = tasi['date'],
                              y = tasi['close'],
                              name='close'
                              )
                    )
     fig.layout.update(title_text = 'TASI index',
                         xaxis_rangeslider_visible=True)

     fig.update_traces(mode="lines", hovertemplate=None)
     fig.update_layout(hovermode="x unified")

     st.plotly_chart(fig)

def plot_raw_data(data):
     fig = go.Figure()
     fig.add_trace(go.Scatter(x = data['transactionDateStr'],
                              y = data['todaysOpen'],
                              name='open'
                              )
                    )

     fig.add_trace(go.Scatter(x = data['transactionDateStr'],
                              y = data['lastTradePrice'],
                              name='close'
                              )
                    )
     fig.layout.update(title_text = data['stock name'].iloc[0],title_x=0.5,
                         xaxis_rangeslider_visible=True)
     fig.update_traces(mode="lines", hovertemplate=None)
     fig.update_layout(hovermode="x unified")
     st.plotly_chart(fig)


def plotForecast(forecast,data):
     forecast_fig = go.Figure()

     forecast_fig.add_trace(go.Scatter(x = forecast['ds'],
                                   y = forecast['yhat_lower'],
                                   fill=None,
                                   mode='lines',
                                   line_color='lightblue',
                                   showlegend = False,
                                   hoverinfo='skip'
                              ))
     forecast_fig.add_trace(go.Scatter(x = forecast['ds'],
                                   y = forecast['yhat_upper'],

                                   fill='tonexty', # fill area between trace0 and trace1
                                   mode='lines',
                                   line_color='lightblue',
                                   showlegend=False,
                                   hoverinfo='skip'))



     forecast_fig.add_trace(go.Scatter(x = data['transactionDateStr'],
                                   y = data['lastTradePrice'],
                                   name = 'actual',
                                   line_color='black'
                                   )
                    )
     forecast_fig.add_trace(go.Scatter(x = forecast['ds'],
                                   y = forecast['yhat'].round(2),
                                   name = 'forecast',
                                   line_color='blue',
                                   )
                    )

     forecast_fig.layout.update(title_text = data['stock name'].iloc[0],title_x=0.5,
                         xaxis_rangeslider_visible=True)
     forecast_fig.update_traces(mode="lines", 
                              hovertemplate=None)
     
     forecast_fig.update_layout(hovermode="x unified")

     st.plotly_chart(forecast_fig)




@st.cache
def getTASI(startDate,endDate,start):
    startDate = startDate.replace('-','/')
    endDate = endDate.replace('-','/')
    url = f"https://www.saudiexchange.sa/wps/portal/tadawul/markets/equities/indices/today/!ut/p/z1/rZJdT8IwFIZ_ixe9lJ7BBPWuMWHWTCKR4ezNUroqM_1YusLw31u4M9GigXPXnOdJ874tZrjEzPBt8859Yw1X4fzKxtVweHed3KSQQz5JgIwzoPPHdJRNAb_EAMgSzP7lZ3Q2ATIn98vpchH80Wk-pH_z4ZchcNxnUWSWxIFDRd-BHzqIAvuQByCS4uFYjvDQa-_bWwQI-r4fNCs9EFYj2GllOgStszWCmnvuP1uJQFjjpfEInOzsxgl5KaxSUuz_TYeZ5ytqarnD5ZN0b9ZpboQ89yVizZ2vPO-aSmycC2TVhaV1uFyQZ4pbXRRFCQ39uFLbnFx8AZWL71c!/p0/IZ7_NHLCH082KGN530A68FC4AN2OM2=CZ6_22C81940L0L710A6G0IQM43GF0=N/?start={start}&length=30&sourceCallerId=datePicker&dateParameter={startDate}+-+{endDate}&typeOfCall=adjustedType"

    payload={}
    headers = {
      'Cookie': 'BIGipServerSaudiExchange.sa.app~SaudiExchange.sa_pool=1560223660.20480.0000; TS0155930d=0102d17fadc9386dd38ca437e88c8a3a7cb83ead3d57e8bdf31fbe396e94b7f8ae94323d9db8295d6f7fcadb8d87d7ab02ec0515a0407a40d8e9e18abf6fedfe30a1f3a137'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    resp_json = json.loads(response.text)
    df = pd.DataFrame(resp_json['data'])
    return df

def getTasiIndex(startDate,endDate):
    df = []
    days = (pd.to_datetime(endDate)-pd.to_datetime(startDate)).days
    for start in range(0,days,10):
        
        df2 = getTASI(startDate.replace('-','/'),endDate.replace('-','/'),start)
        df.append(df2)

    df = pd.concat(df).reset_index()
    df['date'] = pd.to_datetime(df['date'])
    return df

def getSymbols():
    url = "https://www.saudiexchange.sa/tadawul.eportal.theme.helper/ThemeSearchUtilityServlet"

    payload={}
    files={}
    headers = {
      'Referer': 'https://www.saudiexchange.sa/wps/portal/tadawul/markets/equities/market-watch/market-watch-today?',
      'lang': 'en',
      'server': 'nginx/1.14.1',
      'requestTime': '2022-12-01-30-01',
      'Cookie': 'BIGipServerSaudiExchange.sa.app~SaudiExchange.sa_pool=1560223660.20480.0000; TS0155930d=0102d17fad65000806277ea912393fce0b6b4a9fe149650b61229347fbb2f6c75182ce97619ee3dcbf5628a68ef5a982316ab039f312f9f2f30ee198bd1ec9ba38347821df'
    }

    response = requests.request("GET", url, headers=headers, data=payload, files=files)

    df = json.loads(response.text)
    df = pd.DataFrame(df)
    return df

def fetchData(start,symbol,startDate,endDate,l=30):
    
    url = "https://www.saudiexchange.sa/wps/portal/tadawul/market-participants/issuers/issuers-directory/company-details/!ut/p/z1/pZJvT8IwEIc_zV73aDc2fFe7uc6NJQWKrG9MQQSS_QsOzfj0lmFiSGRivHeXPM9d7pdDCi2QKvX7bqObXVXq3PSZGj6nPGEcPByHwYwAHfpjNkkjDADoqQMwZt5gZEMCiTswQAiRGNsEBEHqT34YpS5QQfn8YW5QD__PB_s2H64Uhd_8zPjuNwBSjgxAmBC-gyF00BQppN7Wer_aisN636LMJuS0V12OBo59YwZx7DNj3jtfQF-0l8AP2fUCp3A6oOf6R6Q2ebU8f8K2aeo7Cyxo9Iv-OOSWSWdVFbUu22lbLCsDdbfVhZRycZy91sGEHxP6CYiftRU!/p0/IZ7_NHLCH082KGET30A6DMCRNI2086=CZ6_NHLCH082KGET30A6DMCRNI2000=NJhistoricalPerformance=/"

    payload={'startDate': startDate,
    'toDate': endDate,
    'start': str(start),
    'length': str(l),
    'symbol': str(symbol),
    'draw': '1'}
    files=[

    ]
    headers = {
    'symbol': str(symbol),
    'path': '/wps/portal/tadawul/market-participants/issuers/issuers-directory/company-details/!ut/p/z1/pZJvT8IwEIc_zV73aDc2fFe7uc6NJQWKrG9MQQSS_QsOzfj0lmFiSGRivHeXPM9d7pdDCi2QKvX7bqObXVXq3PSZGj6nPGEcPByHwYwAHfpjNkkjDADoqQMwZt5gZEMCiTswQAiRGNsEBEHqT34YpS5QQfn8YW5QD__PB_s2H64Uhd_8zPjuNwBSjgxAmBC-gyF00BQppN7Wer_aisN636LMJuS0V12OBo59YwZx7DNj3jtfQF-0l8AP2fUCp3A6oOf6R6Q2ebU8f8K2aeo7Cyxo9Iv-OOSWSWdVFbUu22lbLCsDdbfVhZRycZy91sGEHxP6CYiftRU!/p0/IZ7_NHLCH082KGET30A6DMCRNI2086=CZ6_NHLCH082KGET30A6DMCRNI2000=NJhistoricalPerformance=/',
    'Authority': 'www.saudiexchange.sa',
    'Referer': f'https://www.saudiexchange.sa/wps/portal/tadawul/market-participants/issuers/issuers-directory/company-details/!ut/p/z1/04_Sj9CPykssy0xPLMnMz0vMAfIjo8zi_Tx8nD0MLIy83V1DjA0czVx8nYP8PI0MDAz0I4EKzBEKDEJDLYEKjJ0DA11MjQzcTfXDCSkoyE7zBAC-SKhH/?companySymbol={symbol}',
    'scheme': 'https',
    'Cookie': 'BIGipServerSaudiExchange.sa.app~SaudiExchange.sa_pool=1560223660.20480.0000; TS0155930d=0102d17fad65000806277ea912393fce0b6b4a9fe149650b61229347fbb2f6c75182ce97619ee3dcbf5628a68ef5a982316ab039f312f9f2f30ee198bd1ec9ba38347821df'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    return response.text

def getDataFromSymbol(symbol,startDate=None,toDate=None):
    if startDate is None:
        startDate = datetime.datetime(datetime.datetime.now().year,1,1).strftime('%Y-%m-%d')
    if toDate is None: 
        toDate = datetime.datetime.now().strftime('%Y-%m-%d')
        
    days = (pd.to_datetime(toDate)-pd.to_datetime(startDate)).days
    df = []
    length = 30;
    print(f'fetching symbol {symbol} data from {startDate} to {toDate}')
    for start in range(0,days,length):
        # resp = fetchData(symbol,startDate,toDate,start,length)
        resp = fetchData(start,symbol,startDate,toDate,length)
        respjson = json.loads(resp)
        df_temp = pd.DataFrame(respjson['data'])
        df.append(df_temp)
    
    df = pd.concat(df)
    df.insert(0,'symbol', symbol)
    if len(df) > 0:
        df['transactionDateStr'] = pd.to_datetime(df['transactionDateStr'])
        df.insert(1,'day',df['transactionDateStr'].apply(lambda v: day_name[v.weekday()]))
    else:
        print(symbol,'does not have data')
    return df.reset_index()










sym_df = getSymbols()#st.cache(getSymbols)()
# tasi = getTasiIndex('2022-01-01','2022-03-01')

sym_df = sym_df.drop(columns='bond_type').dropna()
st.title("stock display app")

stocks = sym_df['companyNameAR'].values

selected_stocks = st.selectbox("Select stocks",stocks)

col1, col2 = st.columns(2)

startDate = col1.date_input(
     "select start date",
     date(2020,9, 1))

endDate = col2.date_input(
     "select start date",
     date(2021, 9, 1),
     min_value=date(2018,1,1))

print(startDate,endDate)


cols = st.columns(2)

period = cols[0].slider("days of prediction",7,60,30)
cols[1].slider("slider for fun :)",7,100,50)
@st.cache
def load_data(selected_stock):
    symbol = sym_df.loc[sym_df['companyNameAR']==selected_stocks,'symbol'].iloc[0]
    df = getDataFromSymbol(symbol,startDate,endDate)
    df.reset_index(inplace=True)
    df.insert(0,'stock name', selected_stock)
    return df.drop(columns=['level_0','index','symbol'])

data_load_state = st.text("Loading data...")
data = load_data(selected_stocks)
data_load_state.text("Loading data...done!")

st.subheader("Data")
df = data
if 'transactionDataStr' in data.columns:
     df = data.drop(columns='transactionDateStr')

st.dataframe(df.head(20),width=900)

plot_raw_data(data)
# plot_tasi(tasi)

@st.cache
def forecastFunc(data):
     m = Prophet()
     df_train = data[['transactionDateStr','lastTradePrice']]
     df_train.rename(columns={'transactionDateStr' : "ds",
                              "lastTradePrice"     : "y" 
                              },inplace=True)

     m.fit(df_train)

     future = m.make_future_dataframe(periods=period)
     forecast = m.predict(future)
     forecast.insert(1,'Day',forecast['ds'].apply(lambda v: calendar.day_name[v.weekday()]))
     
     return m,forecast



