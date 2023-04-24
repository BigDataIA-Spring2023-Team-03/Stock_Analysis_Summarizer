import streamlit as st
import pandas as pd
import openpyxl
import yfinance as yf
import requests
from datetime import datetime
# import snowflake.connector
from Util import db_util

# Function to ask a companies ticker symbol
def get_ticker(company_name):
    url = "https://api.openai.com/v1/engines/text-davinci-002/completions"
    Ticker = {
        "prompt": "Q: What is the ticker for" + " " + company_name + "?",
        "temperature": 0.7,
        "max_tokens": 50,
        "stop": None
    }

    # set up the API headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer YOUR_KEY"
    }

    # send the API request
    response = requests.post(url, json=Ticker, headers=headers)

    # Exception Handeling
    if response.status_code == 200:
        data = response.json()
        generated_text = data["choices"][0]["text"]        
        ticker_symbol = generated_text.split()
        st.write(ticker_symbol[-1])
    else:
        st.write("Error:", response.text)

# Function to validate the ticker symbol
def validate_ticker(ticker):
    try:
        data = yf.Ticker(ticker)
        info = data.info
    except:
        return False
    return True

# Function to add ticker manually
def add_data(ticker):
    st.session_state['portfolio'] = st.session_state['portfolio'].append({'Stock_Ticker': ticker}, ignore_index=True)

##############################################################################################################################

def portfolio_uploader():
    # Title of the page
    st.title("Stock Analysis Summarizer")

    # Uploading User Stock Portfolio
    excel_upload = st.checkbox('Upload Portfolio from File')
    if excel_upload:
        file = st.file_uploader("**Upload your Stock Portfolio**", type=["xlsx"])

    # Initialize
    if "portfolio" not in st.session_state:
        st.session_state['portfolio'] = pd.DataFrame(columns=['Stock_Ticker'])

    # Manually add tickers
    manual_upload = st.checkbox('Manually Upload Portfolio')

    if manual_upload:
        # Get companies ticker symbol from ChatGPT
        company_name = st.text_input("Enter Company Name for Ticker Symbol")
        if company_name:
            get_ticker(company_name)

        # Adding ticker manually
        portfolio = pd.DataFrame(columns=['Stock_Ticker'])

        # Only can run 5 stocks at a time
        if st.session_state['portfolio'].shape[0] <= 4:

            ticker = st.text_input("Enter a ticker:")

            if ticker:
                # Add Validation check for the ticker from Yahoo finanace
                if validate_ticker(ticker):
                    st.write(f"{ticker} is a valid ticker symbol.")
                    # Adding the ticker manually
                    add_data(ticker)
                    st.session_state['portfolio'] = st.session_state['portfolio']
                else:
                    st.write(f"{ticker} is not a valid ticker symbol.")
        else:
            st.error('You can only run 5 stocks at a time!')


        # Remove a ticker from the portfolio
        for i, ticker in enumerate(st.session_state['portfolio']['Stock_Ticker']):
            if st.button(f"Remove {ticker}", key=f"remove_{i}"):
                st.session_state['portfolio'] = st.session_state['portfolio'].drop(index=i).reset_index(drop=True)

        # Display portfolio after removal
        st.write(st.session_state['portfolio'])

    #############################################################################################################################

    # Run Analysis
    run_analysis = st.checkbox('Run Analysis')

    if run_analysis:
        # TODO:
        st.write('INSERT INTO SNOWFLAKE AND TRIGGER DAG')

        # iterate through the values in the 'Stock_Ticker' column using iteritems()
        for index, value in st.session_state['portfolio']['Stock_Ticker'].iteritems():
            st.write(value)
            service_plan = 'test'
            result = 'test'
            # add_run(st.session_state['logged_in_user'], stock, service_plan, result)
            # add_run('test_user', value, service_plan, result)
            db_util.add_stock_run('test_user', value, service_plan, result)



            # TODO: Call the DAG via FastAPI

            # Possible results
            # result = ['BUY', 'SELL', 'NO DATA FOUND', 'ERROR]
        


#############################################################################################################################


# # If the user has uploaded a file
# if file is not None:
#     # Read the Excel file into a Pandas DataFrame
#     df = pd.read_excel(file, sheet_name='Sheet1')
#     # Display the contents of the DataFrame
#     st.write(df)

# # Selecting Ticker for Analysis from the List Available
# add_item = st.text_input("**Add Ticker**")
# if add_item:
#     # Load the Excel file
#     workbook = openpyxl.load_workbook("C:/Users/rumij/Downloads/ticker.xlsx")
#     # Select the worksheet you want to add the item to
#     worksheet = workbook["Sheet1"]
#     # Add a new item to the worksheet
#     new_item = add_item
#     worksheet.append([new_item])
#     # Save the changes to the Excel file
#     workbook.save("C:/Users/rumij/Downloads/ticker.xlsx")

# remove_item = st.text_input("**Delete a Ticker**")
# if remove_item:
#     # Load the Excel file
#     workbook = openpyxl.load_workbook("C:/Users/rumij/Downloads/ticker.xlsx")
#     # Select the worksheet you want to add the item to
#     worksheet = workbook["Sheet1"]
#     # Add a new item to the worksheet
#     for row in worksheet.iter_rows():
#         for cell in row:
#             if cell.value == remove_item:
#             #     # Delete the row containing the cell
#                 worksheet.delete_rows(cell.row)
#                 # Save the changes to the Excel file
#                 workbook.save("C:/Users/rumij/Downloads/ticker.xlsx")
#                 break  # Exit the inner loop after deleting the row

# my_list = []
# stocks = pd.read_excel('C:/Users/rumij/Downloads/ticker.xlsx')
# stocks = stocks['Ticker'].unique()
# # selected_option = st.selectbox("**Select an option**", stocks)
# selected_option = st.multiselect("**Select Any 5 Tickers for Analysis**", stocks, max_selections=2)

# # my_list.append(selected_option)
# my_list = 'You selected: ' + ', '.join(selected_option)

# st.write(my_list)
