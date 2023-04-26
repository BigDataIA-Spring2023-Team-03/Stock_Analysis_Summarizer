from Util import db_conn
from datetime import datetime
import pandas as pd

# from Authentication import auth

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
    with db_conn.get_conn().cursor() as cur:
        cur.execute(
            "INSERT INTO USERS (EMAIL, PASSWORD, SIGNUP_DATE, SERVICE_PLAN, ADMIN_FLAG) VALUES (%s, %s, %s, %s, %s)",
            (email, password_hash, timestamp, service_plan, admin_flag)
        )

# def check_user(email: str, password: str):
#     conn = db_conn.get_conn()
#     query = f"SELECT email, password FROM USERS  WHERE email = '{email}'"
#     try:
#         with conn.cursor() as cur:
#             cur.execute(query)
#             count = cur.fetchone()
#         return auth.verify_password(password, count[1])
#     except Exception as e:
#         raise Exception("Error during query execution", e)
    
#Add new user to db
def add_stock_run(email, stock, service_plan, result):
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")
    with db_conn.get_conn().cursor() as cur:
        cur.execute(
            f"""INSERT INTO logging (email, run_date, stock, service_plan, result) 
              VALUES ('{email}', '{timestamp}', '{stock}', '{service_plan}', '{result}')"""
             )
        
# Read table into df
def select_table(table_name: str):
    with db_conn.get_conn().cursor() as cur:
        cur.execute(f'select * from STOCK_ANALYSIS_APP.PUBLIC.{table_name}'
        )
        # Fetch all the results into a Pandas DataFrame
        df = pd.DataFrame(cur.fetchall())
        # Set the column names to match the table schema
        df.columns = [desc[0] for desc in cur.description]

    # testing 
    # print(df)

    return df


