import os
import streamlit as st
import boto3
from botocore.errorfactory import ClientError
import requests
import time
import json
import pandas as pd
from datetime import datetime, timedelta
from decouple import config
from Util import db_util




def admin_dashboard():
    # Set the title of the app
    st.title("Admin Dashboard")
    st.write('This dashboard shows history of the app.')

    # Enter Password to Access Page
    password = st.text_input("Enter Password:")

    if password != '':
        if password == 'damgadmin': 
            #############################################################################
            # USER HISTORY
            st.subheader('User History')

            df = db_util.user_history_dashboard()
            st.write(df)

            #############################################################################
            # Stock HISTORY
            st.subheader('Stock History')

            df = db_util.stock_history_dashboard()
            st.write(df)

            #############################################################################
            # Overall Usage HISTORY
            st.subheader('Overall Usage History')
            
            df = db_util.usage_history_dashboard()
            st.write(df)
            
        else:
            st.error("You don't have permission to access this functionality")