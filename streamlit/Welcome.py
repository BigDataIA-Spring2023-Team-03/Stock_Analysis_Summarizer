import streamlit as st
import requests
import time
from streamlit_extras.switch_page_button import switch_page

if 'access_token' not in st.session_state:
    st.session_state.access_token = ''

if 'current_page' not in st.session_state:
    st.session_state.current_page = 'welcome'

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
            # switch_page('portfolio uploader')
        else:
            st.error('Invalid email or password')

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


def main():
    page = st.sidebar.selectbox('Select a page', ['Login', 'Register'])

    if st.session_state.access_token:
        response = requests.get("http://localhost:8000/user_info", params={'token': st.session_state.access_token})
        email = response.json().get('email')
        if email:
            st.sidebar.write(f"Logged in as: {email}")

    if page == 'Login':
        login()
    elif page == 'Register':
        register()

if __name__ == '__main__':
    main()
