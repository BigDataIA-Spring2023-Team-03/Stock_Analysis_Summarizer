import streamlit as st
import yfinance as yf
import plotly.express as px
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objs as go
from Util import db_util


################################################################################################
def analysis_vs_reality():
    # st.set_page_config(page_title='Stock Price Dashboard', page_icon=':chart_with_upwards_trend:', layout='wide', initial_sidebar_state='expanded')
    st.title('Analysis vs. Reality')

    st.write('The Options Below are Based Off of Your Previous Runs of the APP:')
    # Get Tickers and dates of previous runs
    df = db_util.user_history(st.session_state.email)
    stock_list = df['STOCK'].tolist()
    stock_list = list(set(stock_list))
    
    selected_stock = st.selectbox('Select a stock', stock_list)
    if selected_stock:
        date_list = []
        date_list.append(df.loc[df['STOCK'] == selected_stock, 'RUN_DATE'].item())
        date_list = list(set(date_list))

        selected_date = st.selectbox('Select a date of analysis', date_list)

    # Get data from logging table
    analysis_df = db_util.analysis_results(st.session_state.email, selected_stock, selected_date)
    st.write(analysis_df)

    # TODO: Add performance metrics since the run_date

    # TODO: Use the run dates in the graphs below

    options = ['1 month', '6 months', '1 year', 'Full history', 'Custom']
    selected_option = st.selectbox('Select time range:', options)

    if selected_option == 'Custom':
        start_date = st.date_input('Enter custom start date:')
    else:
        start_date = None

    if selected_stock:
        if selected_option == 'Full history':
            data = yf.Ticker(selected_stock).history(period='max')
        elif selected_option == 'Custom' and start_date:
            data = yf.download(selected_stock, start=start_date)
        else:
            data = yf.download(selected_stock)
        
        if selected_option == '1 month':
            data = data.loc[pd.to_datetime('today') - pd.DateOffset(months=1):]
        elif selected_option == '6 months':
            data = data.loc[pd.to_datetime('today') - pd.DateOffset(months=6):]
        elif selected_option == '1 year':
            data = data.loc[pd.to_datetime('today') - pd.DateOffset(years=1):]
        
        fig = make_subplots(rows=1, cols=1)
        fig.add_trace(go.Scatter(x=data.index, y=data['Close'], name='Close', line=dict(color='royalblue', width=2)))
        fig.update_layout(title=f'{selected_stock} Stock Price', xaxis_title='Date', yaxis_title='Price ($)', font=dict(family='Courier New, monospace', size=18, color='#7f7f7f'))
        st.plotly_chart(fig)