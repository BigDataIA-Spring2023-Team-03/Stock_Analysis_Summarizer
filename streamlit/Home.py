import streamlit as st
from components import login, register, portfolio_uploader, admin_dashboard, analysis_vs_reality
import requests

# Check if the user is logged in
if 'access_token' not in st.session_state:
    st.session_state.access_token = ''

# Define a function to render the sidebar
def render_sidebar():
    st.sidebar.title("Navigation")
    if st.session_state.access_token == '':
        selected_page = st.sidebar.selectbox("Select a page", ["Login", "Register"])
    else:
        selected_page = st.sidebar.selectbox("Select a page", ["Portfolio Uploader", "Analysis vs Reality", "Admin Dashboard"])
        response = requests.get("http://localhost:8000/user_info", params={'token': st.session_state.access_token})
        email = response.json().get('email')
        if email:
            st.sidebar.write(f"Logged in as: {email}")
        if st.sidebar.button('Logout'):
            st.session_state.access_token = ''
            st.experimental_rerun()
    return selected_page

# Render the sidebar
selected_page = render_sidebar()

# Render the selected page
if selected_page == 'Login':
    login.login()

elif selected_page == 'Register':
    register.register()

elif selected_page == 'Portfolio Uploader':
    # portfolio_uploader.portfolio_uploader()
    pass

elif selected_page == 'Analysis vs Reality':
    # portfolio_uploader.portfolio_uploader()
    pass

elif selected_page == 'Admin Dashboard':
    # portfolio_uploader.portfolio_uploader()
    pass
