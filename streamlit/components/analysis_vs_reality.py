import streamlit as st
import yfinance as yf
import plotly.express as px
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objs as go


def analysis_vs_reality():
    # st.set_page_config(page_title='Stock Price Dashboard', page_icon=':chart_with_upwards_trend:', layout='wide', initial_sidebar_state='expanded')
    st.title('Analysis vs. Reality')

    # TODO: Display the tickers a user has run before using logging table in Snowflake
    # f"""
    # SELECT *
    # FROM LOGGING
    # where email = '{email}';
    # """
    ticker = st.text_input('Enter stock ticker (e.g. AAPL, NVDA):')

    # TODO: Get the run_dates for those analyses using logging in snowflake

    options = ['1 month', '6 months', '1 year', 'Full history', 'Custom']
    selected_option = st.selectbox('Select time range:', options)

    if selected_option == 'Custom':
        start_date = st.date_input('Enter custom start date:')
    else:
        start_date = None

    if ticker:
        if selected_option == 'Full history':
            data = yf.Ticker(ticker).history(period='max')
        elif selected_option == 'Custom' and start_date:
            data = yf.download(ticker, start=start_date)
        else:
            data = yf.download(ticker)
        
        if selected_option == '1 month':
            data = data.loc[pd.to_datetime('today') - pd.DateOffset(months=1):]
        elif selected_option == '6 months':
            data = data.loc[pd.to_datetime('today') - pd.DateOffset(months=6):]
        elif selected_option == '1 year':
            data = data.loc[pd.to_datetime('today') - pd.DateOffset(years=1):]
        
        fig = make_subplots(rows=1, cols=1)
        fig.add_trace(go.Scatter(x=data.index, y=data['Close'], name='Close', line=dict(color='royalblue', width=2)))
        fig.update_layout(title=f'{ticker} Stock Price', xaxis_title='Date', yaxis_title='Price ($)', font=dict(family='Courier New, monospace', size=18, color='#7f7f7f'))
        st.plotly_chart(fig)