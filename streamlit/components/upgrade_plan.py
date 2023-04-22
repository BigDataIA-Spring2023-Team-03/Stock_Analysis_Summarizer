import streamlit as st
import requests
import time

def upgrade_plan(email: str):
    st.title('Update Service Plan')
    st.write(f'Current Service Plan: {get_service_plan(email)["service_plan"]}')
    l = ['FREE', 'GOLD', 'PLATINUM']
    updated_plan = st.selectbox("Select a plan", [i for i in l if not i == get_service_plan(email)["service_plan"]])
    if st.button('Submit'):
        update_service_plan(email, updated_plan, l)

def get_service_plan(email: str):
    if email and not email == "":
        response = requests.get("http://localhost:8000/user_data", params={'email': email})
        return response.json()

def update_service_plan(email, updated_plan: str, l):
    if updated_plan and updated_plan in l:
        data = {'service_plan': updated_plan, 'email': email}
        response = requests.post("http://localhost:8000/update_plan", json=data)
        if response.status_code == 200:
            st.success('Service Plan Updated for {}'.format(email))
            time.sleep(1)
            st.session_state.access_token = ''
            st.session_state.email = ''
            st.experimental_rerun()
        elif response.status_code == 403:
            st.error('Session ended, please login back')
            time.sleep(1)
            st.session_state.access_token = ''
            st.session_state.email = ''
            st.experimental_rerun()
