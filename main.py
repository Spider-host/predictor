# pip install streamlit fbprophet yfinance plotly
import streamlit as st
from datetime import date
import pandas as pd
import yfinance as yf
import streamlit as st
import numpy as np
import chart_studio.plotly as plotly
import plotly.figure_factory as ff
from plotly import graph_objs as go
from prophet import Prophet
from prophet.plot import plot_plotly

switch = st.checkbox("LIVE DATA")
if switch:
    st.write("LIVE UPDATES IN STOCKS...")

    START = "2010-01-01"
    TODAY = date.today().strftime("%Y-%m-%d")

    st.title('Stock Trend Predictor')
    st.text("created by CECians...")

    stocks = ('GOOG', 'AAPL', 'MSFT', 'GME', 'TCS.NS')
    selected_stock = st.selectbox('Select dataset for prediction', stocks)

    n_years = st.slider('Years of prediction:', 1, 5)
    period = n_years * 365 



 
    def load_data(ticker):
         data = yf.download( ticker, START, TODAY)
         data.reset_index(inplace=True)
         return data

	
    data_load_state = st.text('Loading data...')
    data = load_data(selected_stock)
    data_load_state.text('Loading data... done!')

    st.subheader('Raw data')
    st.write(data.tail())
    

    def plot_raw_data():
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="stock_open"))
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="stock_close"))
        fig.layout.update(title_text='Time Series data with Rangeslider', xaxis_rangeslider_visible=True)
        st.plotly_chart(fig)
	
     
   
	
    plot_raw_data()

     # Predict forecast with Prophet.
    df_train = data[['Date','Close']]
    df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

    m = Prophet()
    m.fit(df_train)
    future = m.make_future_dataframe(periods=period)
    forecast = m.predict(future)

    # Show and plot forecast
    st.subheader('Forecast data')
    st.write(forecast.tail())
    
    st.write(f'Forecast plot for {n_years} years')
    fig1 = plot_plotly(m, forecast)
    st.plotly_chart(fig1)

    st.write("Forecast components")
    fig2 = m.plot_components(forecast)
    st.write(fig2)

else:
    st.write("BASED ON HISTORICAL DATA...")

    st.title('Stock Forecast App')

    dataset = ("ADANIENT","AXISBANK","CANBK","BAJFINANCE","SUNTV","TATAMOTORS","TVSMOTOR","VGUARD","VOLTAS","WIPRO","SIEMENS")
    selected_stock = st.selectbox('Select dataset for prediction',dataset)
    DATA_URL = ('./HISTORICAL_DATA/'+selected_stock+'_data.csv')

    year = st.slider('Year of prediction:',1,4)
    period = year * 365
     
    

    # @st.cache_data
    def load_data():
        data = pd.read_csv(DATA_URL)
        return data
	


    data_load_state = st.text('Loading data...')
    data = load_data()
    data_load_state.text('Loading data... done!')

    def plot_raw_data():
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data['Date'], y=data['open'], name="stock_open"))
        fig.add_trace(go.Scatter(x=data['Date'], y=data['close'], name="stock_close"))
        fig.layout.update(title_text='Time Series data with Rangeslider', xaxis_rangeslider_visible=True)
        st.plotly_chart(fig)
	   
    if st.checkbox('Show raw data'):
        st.subheader('Raw data')
        st.write(data)
	
    # plotting the figure of Actual Data
    plot_raw_data()

    # preparing the data for Facebook-Prophet.

    data_pred = data[['Date','close']]
    data_pred=data_pred.rename(columns={"Date": "ds", "close": "y"})

    # code for facebook prophet prediction

    m = Prophet()
    m.fit(data_pred)
    future = m.make_future_dataframe(periods=period)
    forecast = m.predict(future)

    #plot forecast
    fig1 = plot_plotly(m, forecast)
    if st.checkbox('Show forecast data'):
        st.subheader('forecast data')
        st.write(forecast)
        st.write('Forecasting closing of stock value for'+selected_stock+' for a period of: '+ str(year) +'year')
    st.plotly_chart(fig1)

    #plot component wise forecast
    st.write("Component wise forecast")
    fig2 = m.plot_components(forecast)
    st.write(fig2)
