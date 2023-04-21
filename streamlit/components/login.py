import streamlit as st
import requests

def login():
    email = st.text_input('Email')
    password = st.text_input('Password', type='password')
    if st.button('Login'):
        data = {'email': email, 'password': password}
        response = requests.post('http://localhost:8000/user/login', json=data)
        if response.status_code == 200:
            access_token = response.json().get("access_token")
            st.session_state.access_token = access_token
            st.success('Logged in as {}'.format(email))
            if access_token:
                st.experimental_rerun()
        else:
            st.error('Invalid email or password')