import streamlit as st
import requests
import time
from email_validator import validate_email, EmailNotValidError

def register():
    st.title('Register Page')

    def check_email(email):
        try:
        # validate and get info
            v = validate_email(email)
            # replace with normalized form
            email = v["email"] 
            # print("True")
            return True
        except EmailNotValidError as e:
            # email is not valid, exception message is human-readable
            # st.error(str(e))
            return str(e)

    email = st.text_input('Email')
    password = st.text_input('Password', type='password')
    confirm_password = st.text_input('Confirm Password', type='password')
    service_plan = st.selectbox('Service Plan', ['FREE', 'GOLD', 'PLATINUM'])
    admin_flag = st.checkbox('Admin Flag')

    # if check_email(email) == True and st.button('Register'):
    if password == confirm_password and st.button('Register'):
        if check_email(email) == True:
            data = {'email': email, 'password': password, 'service_plan': service_plan, 'admin_flag': admin_flag}
            response = requests.post('http://localhost:8000/user/register', json=data)
            if response.status_code == 200:
                st.success('Account created for {}'.format(email))
                time.sleep(3)
                st.experimental_rerun()
            else:
                st.error('Failed to create account')
        else:
            st.error(f'Invalid Email: {check_email(email)}')
    elif not password == confirm_password and st.button('Register'):
        st.error('Passwords don\'t match')
        time.sleep(3)
        st.experimental_rerun()