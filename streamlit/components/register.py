import streamlit as st
import requests
import time

def register():
    email = st.text_input('Email')
    password = st.text_input('Password', type='password')
    confirm_password = st.text_input('Confirm Password', type='password')
    service_plan = st.selectbox('Service Plan', ['Basic', 'Premium', 'Enterprise'])
    admin_flag = st.checkbox('Admin Flag')
    if password == confirm_password and st.button('Register'):
        data = {'email': email, 'password': password, 'service_plan': service_plan, 'admin_flag': admin_flag}
        response = requests.post('http://localhost:8000/user/register', json=data)
        if response.status_code == 200:
            st.success('Account created for {}'.format(email))
            time.sleep(3)
            st.experimental_rerun()
        else:
            st.error('Failed to create account')
    elif not password == confirm_password and st.button('Register'):
        st.error('Passwords don\'t match')
        time.sleep(3)
        st.experimental_rerun()