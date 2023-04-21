import streamlit as st
from components import login, register, portfolio_uploader, dummy

# Check if the user is logged in
if 'access_token' not in st.session_state:
    st.session_state.access_token = ''
    page = 'Login'
else:
    page = 'Dummy'

# Define a function to render the sidebar
def render_sidebar():
    st.sidebar.title("Navigation")
    if st.session_state.access_token == '':
        selected_page = st.sidebar.selectbox("Select a page", ["Login", "Register"])
    else:
        selected_page = st.sidebar.selectbox("Select a page", ["Portfolio Uploader", "Dummy"])

    return selected_page

# Render the sidebar
selected_page = render_sidebar()

# Render the selected page
if selected_page == 'Welcome':
    st.title("Welcome to my app!")
    st.write("Please log in or register to use the app.")

elif selected_page == 'Login':
    login.login()

elif selected_page == 'Register':
    register.register()

elif selected_page == 'Portfolio Uploader':
    portfolio_uploader.portfolio_uploader()

elif selected_page == 'Dummy':
    dummy.dummy()
