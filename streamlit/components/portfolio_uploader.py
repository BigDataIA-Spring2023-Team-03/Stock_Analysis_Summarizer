import streamlit as st
import pandas as pd
import openpyxl
# import os
# import requests
def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://static.seekingalpha.com/cdn/s3/uploads/getty_images/1057996634/image_1057996634.jpg?io=getty-c-w1280.jpg");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

add_bg_from_url()

# Uploading User Stock Portfolio
file = st.file_uploader("**Upload your Stock Portfolio**", type=["xlsx"])

# Initialize
if "portfolio" not in st.session_state:
    st.session_state['portfolio'] = pd.DataFrame(columns=['Stock_Ticker'])

# Manually add tickers
manual_upload = st.checkbox('Manually Upload Portfolio')

def add_data(ticker):
    st.session_state['portfolio'] = st.session_state['portfolio'].append({'Stock_Ticker': ticker}, ignore_index=True)

if manual_upload:
    portfolio = pd.DataFrame(columns=['Stock_Ticker'])

    # Only can run 5 stocks at a time
    if st.session_state['portfolio'].shape[0] <= 4:

        ticker = st.text_input("Enter a ticker:")

        if ticker:
            add_data(ticker)
            st.session_state['portfolio'] = st.session_state['portfolio']
    
    else:
        st.error('You can only run 5 stocks at a time!')

    st.write(st.session_state['portfolio'])


# Run Analysis
run_analysis = st.checkbox('Run Analysis')

if run_analysis:
    # TODO:
    st.write('INSERT INTO SNOWFLAKE AND TRIGGER DAG')