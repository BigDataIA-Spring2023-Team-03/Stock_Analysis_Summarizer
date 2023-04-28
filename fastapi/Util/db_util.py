from Util import db_conn
from datetime import datetime

from Authentication import auth

def check_user_exists(email: str) -> bool:
    conn = db_conn.get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM STOCK_ANALYSIS_APP.PUBLIC.USERS WHERE EMAIL = %s", (email,) )
            count = cur.fetchone()[0]
            if count > 0:
                return True
            else:
                return False
    except Exception as e:
        raise e
    finally:
        conn.close()

def insert_user(email: str, password_hash: str, service_plan: str, admin_flag: bool):
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")
    calls_left = 0
    if service_plan == 'FREE':
        calls_left = 10
    elif service_plan == 'GOLD':
        calls_left = 30
    elif service_plan == 'PLATINUM':
        calls_left = 50
    with db_conn.get_conn().cursor() as cur:
        cur.execute(
            "INSERT INTO USERS (EMAIL, PASSWORD, SIGNUP_DATE, SERVICE_PLAN, ADMIN_FLAG) VALUES (%s, %s, %s, %s, %s)",
            (email, password_hash, timestamp, service_plan, admin_flag)
        )
        cur.execute(
            f"INSERT INTO API_CALLS (EMAIL, SERVICE_PLAN, CALLS_LEFT) VALUES ('{email}', '{service_plan}', {calls_left})"
        )

def update_serviceplan(service_plan: str, email: str):
    calls_left = 0
    if service_plan == 'FREE':
        calls_left = 10
    elif service_plan == 'GOLD':
        calls_left = 30
    elif service_plan == 'PLATINUM':
        calls_left = 50
    with db_conn.get_conn().cursor() as cur:
        cur.execute(
            f"UPDATE USERS SET SERVICE_PLAN = '{service_plan}' WHERE email = '{email}'"
        )
        cur.execute(
            f"UPDATE API_CALLS SET CALLS_LEFT = '{calls_left}' WHERE email = '{email}'"
        )
        cur.execute(
            f"UPDATE API_CALLS SET SERVICE_PLAN = '{service_plan}' WHERE email = '{email}'"
        )

def update_api_calls(email: str):
    with db_conn.get_conn().cursor() as cur:
        cur.execute(
            f"SELECT CALLS_LEFT FROM API_CALLS WHERE email = '{email}'"
        )
        calls_left = cur.fetchone()[0]
        cur.execute(
            f"UPDATE API_CALLS SET CALLS_LEFT = '{calls_left - 1}' WHERE email = '{email}'"
        )

def delete_user(email: str):
    with db_conn.get_conn().cursor() as cur:
        cur.execute(
            f"DELETE FROM USERS WHERE email = '{email}'"
        )
        cur.execute(
            f"DELETE FROM API_CALLS WHERE email = '{email}'"
        )

def check_user(email: str, password: str):
    conn = db_conn.get_conn()
    query = f"SELECT email, password FROM USERS  WHERE email = '{email}'"
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            count = cur.fetchone()
        return auth.verify_password(password, count[1])
    except Exception as e:
        raise Exception("Error during query execution", e)

def get_user_data(email: str):
    conn = db_conn.get_conn()
    query = f"SELECT a.service_plan, a.admin_flag, b.calls_left  FROM USERS a left join API_CALLS b on a.email = b.email WHERE a.email = '{email}'"
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            count = cur.fetchone()
            user = {
                'email': email,
                'service_plan': count[0],
                'admin_flag': count[1],
                'calls_left': count[2]
            }
        return user
    except Exception as e:
        raise Exception("Error during query execution", e)
