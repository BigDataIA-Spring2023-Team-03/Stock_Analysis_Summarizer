import streamlit as st
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
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

            # Create a line graph using plotly
            fig = px.line(df, x="SIGNUP_DATE", y="TOTAL_USERS", color="SERVICE_PLAN")

            # Update the layout of the graph
            fig.update_layout(title="Total Users by Signup Date and Service Plan", xaxis_title="Signup Date", yaxis_title="Total Users")

            # Display the graph
            st.plotly_chart(fig)

            #############################################################################
            # Stock HISTORY
            st.subheader('Stock History')

            df = db_util.stock_history_dashboard()
            st.write(df)
            
            # Create a bar graph using plotly
            fig = go.Figure(data=[go.Bar(x=df["STOCK"], y=df["OVERALL_RUNS"])])

            # Update the layout of the graph
            fig.update_layout(title="Overall Runs by Stock", xaxis_title="Stock", yaxis_title="Overall Runs")

            # Display the graph
            st.plotly_chart(fig)

            #############################################################################
            # Overall Usage HISTORY
            st.subheader('Overall Usage History')
            
            df = db_util.usage_history_dashboard()
            st.write(df)
            
        else:
            st.error("You don't have permission to access this functionality")