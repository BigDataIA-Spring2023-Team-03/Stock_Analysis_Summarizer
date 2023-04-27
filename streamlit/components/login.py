import streamlit as st
import requests

# DEV or PROD
environment = 'DEV'
if environment == 'DEV':
    webserver = 'localhost:8000'
elif environment == 'PROD':
    webserver = 'backend:8000'

def login():
    st.title('Login Page')

    email = st.text_input('Email')
    password = st.text_input('Password', type='password')
    if st.button('Login'):
        data = {'email': email, 'password': password}
        response = requests.post(f'http://{webserver}/user/login', json=data)
        if response.status_code == 200:
            access_token = response.json().get("access_token")
            st.session_state.access_token = access_token
            st.success('Logged in as {}'.format(email))
            if access_token:
                st.experimental_rerun()
        else:
            st.error('Invalid email or password')