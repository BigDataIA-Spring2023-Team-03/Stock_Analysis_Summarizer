import streamlit as st
import sqlite3
from cryptography.fernet import Fernet
import os
from datetime import datetime
import snowflake.connector

# Snowflake
# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    return snowflake.connector.connect(
        **st.secrets["snowflake"], client_session_keep_alive=True
    )

conn = init_connection()
c = conn.cursor()

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

rows = run_query("SELECT * from users;")

# Print results.
for row in rows:
    st.write(f"{row[0]} has a :{row[1]}:")


# # Set up SQLite connection
# conn = sqlite3.connect('userinfo.db')
# c = conn.cursor()

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

# decrypt password
def decrypt_password(encrypted_password):
    decrypted_password = cipher_suite.decrypt(encrypted_password).decode()
    return decrypted_password

# Check esisting user
def user_exists(email):
    print(f"SELECT * FROM users WHERE email='{email}'")
    c.execute(f"SELECT * FROM users WHERE email='{email}'")
    result = c.fetchone()
    if result:
        return True
    else:
        return False

#Add new user to db
def add_user(email, password, service_plan, current_time):
    encrypted_password = encrypt_password(password)
    # TODO: Fix encryption for Snowflake
    # print(type(encrypted_password))
    c.execute(f"INSERT INTO users (email, password, service_plan, signup_date) VALUES ('{email}', '{password}', '{service_plan}', '{current_time}')")
    conn.commit()

#Check creds 
def valid_login(email, password):
    c.execute(f"SELECT * FROM users WHERE email='{email}'")
    result = c.fetchone()
    if result:
        encrypted_password = result[1]
        decrypted_password = decrypt_password(encrypted_password)
        # if password == decrypted_password:
        if password == encrypted_password:
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

    email = st.text_input("email")
    password = st.text_input("Password", type='password')

    if st.button("Login"):
        if valid_login(email, password):
            st.success("Logged in as {}".format(email))
            log_activity("{} logged in".format(email))

            st.session_state['logged_in_user'] = email
        else:
            st.warning("Invalid login credentials")
            log_activity("{} failed to log in with email: {} and password: {}".format(email, email, password))

elif choice == "Signup":
    st.subheader("Signup")

    new_email = st.text_input("email")
    new_password = st.text_input("Password", type='password')
    service_plan  = st.selectbox('Choose a Service Plan?', ('Free', 'Gold', 'Premium'))

    if st.button("Signup"):
        if not user_exists(new_email):
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            add_user(new_email, new_password, service_plan, current_time)
            st.success("User created successfully")
            log_activity("{} signed up".format(new_email))
        else:
            st.warning("User already exists")
            log_activity("{} failed to sign up".format(new_email))

elif choice == "Logout":
    if 'logged_in_user' in st.session_state:
        email = st.session_state['logged_in_user']
        del st.session_state['logged_in_user']
        st.success("Logged out successfully")
        log_activity("{} logged out".format(email))
    else:
        st.warning("You are not logged in")

elif choice == "MainApp":
    if 'logged_in_user' in st.session_state:
        with open('abc.py') as f:
            code = compile(f.read(), 'abc.py', 'exec')
            exec(code, {})
    else:
        st.warning("You must be logged in to view this page")
