import streamlit as st 
from datetime import date 
#from fbprophet import Prophet
#from fbprophet.plot import plot_plotly 
import calendar
from tadawulScraper import getTasiIndex,getSymbols, getDataFromSymbol

from plotters import *

sym_df = st.cache(getSymbols)()
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
     "select end date",
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

df = data
if 'transactionDateStr' in data.columns:
     df = data.drop(columns='transactionDateStr')



st.markdown(f"<h2 style='text-align: center;'>{df['stock name'].iloc[0]} </h2>", unsafe_allow_html=True)

st.dataframe(df.drop(columns='stock name').head(20),width=900)

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

     # st.write('forecast components')
     # fig2 = m.plot_components(forecast)
     # fig2.set_size_inches(12,6)
     # st.write(fig2)

#m,forecast = forecastFunc(data)


# st.subheader("Forecast data")
# st.write(forecast.tail(20))

# forecast_fig = plot_plotly(m,forecast)
# forecast_fig.layout.update(title_text = selected_stocks,title_x=0.5,
#                          xaxis_rangeslider_visible=True)

# forecast_fig.update_traces(mode="lines", hovertemplate=None)
# forecast_fig.update_layout(hovermode="x unified")
# st.plotly_chart(forecast_fig)
# plotForecast(forecast,data)
