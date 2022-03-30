from plotly import graph_objs as go 
#from fbprophet import Prophet
#from fbprophet.plot import plot_plotly 
import streamlit as st 


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

