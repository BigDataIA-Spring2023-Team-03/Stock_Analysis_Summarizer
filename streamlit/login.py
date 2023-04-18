import streamlit as st
import sqlite3
from cryptography.fernet import Fernet
import os
from datetime import datetime

# Set up SQLite connection
conn = sqlite3.connect('userinfo.db')
c = conn.cursor()

# Cryptograph setup ~ unique key
key_file = 'key.key'
if os.path.exists(key_file):
    with open(key_file, 'rb') as f:
        key = f.read()
else:
    key = Fernet.generate_key()
    with open(key_file, 'wb') as f:
        f.write(key)
cipher_suite = Fernet(key)

# Encrypt password
def encrypt_password(password):
    encrypted_password = cipher_suite.encrypt(password.encode())
    return encrypted_password

# decrypt pqssword
def decrypt_password(encrypted_password):
    decrypted_password = cipher_suite.decrypt(encrypted_password).decode()
    return decrypted_password

# Check esisting user
def user_exists(username):
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    result = c.fetchone()
    if result:
        return True
    else:
        return False

#Add new user to db
def add_user(username, password):
    encrypted_password = encrypt_password(password)
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, encrypted_password))
    conn.commit()

#Check creds 
def valid_login(username, password):
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    result = c.fetchone()
    if result:
        encrypted_password = result[1]
        decrypted_password = decrypt_password(encrypted_password)
        if password == decrypted_password:
            return True
        else:
            return False
    else:
        return False

#Logging
def log_activity(activity):
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    with open('userlogs.txt', 'a') as f:
        f.write(dt_string + ' - ' + activity + '\n')

st.title("Login Page")

menu = ["Login", "Signup", "Logout", "MainApp"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Login":
    st.subheader("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type='password')

    if st.button("Login"):
        if valid_login(username, password):
            st.success("Logged in as {}".format(username))
            log_activity("{} logged in".format(username))

            st.session_state['logged_in_user'] = username
        else:
            st.warning("Invalid login credentials")
            log_activity("{} failed to log in with username: {} and password: {}".format(username, username, password))

elif choice == "Signup":
    st.subheader("Signup")

    new_username = st.text_input("Username")
    new_password = st.text_input("Password", type='password')

    if st.button("Signup"):
        if not user_exists(new_username):
            add_user(new_username, new_password)
            st.success("User created successfully")
            log_activity("{} signed up".format(new_username))
        else:
            st.warning("User already exists")
            log_activity("{} failed to sign up".format(new_username))

elif choice == "Logout":
    if 'logged_in_user' in st.session_state:
        username = st.session_state['logged_in_user']
        del st.session_state['logged_in_user']
        st.success("Logged out successfully")
        log_activity("{} logged out".format(username))
    else:
        st.warning("You are not logged in")

elif choice == "MainApp":
    if 'logged_in_user' in st.session_state:
        with open('abc.py') as f:
            code = compile(f.read(), 'abc.py', 'exec')
            exec(code, {})
    else:
        st.warning("You must be logged in to view this page")
