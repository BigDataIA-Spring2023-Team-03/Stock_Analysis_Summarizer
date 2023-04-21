import streamlit as st
from components import login, register, portfolio_uploader, admin_dashboard, analysis_vs_reality
import requests

# BACKGROUND
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
    portfolio_uploader.portfolio_uploader()

elif selected_page == 'Analysis vs Reality':
    analysis_vs_reality.analysis_vs_reality()

elif selected_page == 'Admin Dashboard':
    admin_dashboard.admin_dashboard()
