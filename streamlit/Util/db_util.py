from Util import db_conn
from datetime import datetime
import pandas as pd
# import snowflake.connector

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
    
# Add new user to db
def add_stock_run(email, stock, positive_article_count, neutral_article_count, negative_article_count, positive_summary, negative_summary):
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")
    # Escape special characters
    # positive_summary = snowflake.connector.escape_string(positive_summary)
    # positive_summary = positive_summary.replace("'", "\\'")
    # negative_summary = snowflake.connector.escape_string(negative_summary)\
    # negative_summary = negative_summary.replace("'", "\\'")
    with db_conn.get_conn().cursor() as cur:
        cur.execute(
            f"""INSERT INTO logging (email, run_date, stock, positive_article_count, neutral_article_count, negative_article_count, positive_summary, negative_summary) VALUES ('{email}', '{timestamp}', '{stock}', {positive_article_count}, {neutral_article_count}, {negative_article_count}, '{positive_summary}', '{negative_summary}')"""
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


# Get History for user
def user_history(email: str):
    with db_conn.get_conn().cursor() as cur:
        cur.execute(f"""select distinct stock, to_date(run_date) run_date
from STOCK_ANALYSIS_APP.PUBLIC.logging
where email = '{email}'
order by stock, run_date"""
        )
        # Fetch all the results into a Pandas DataFrame
        df = pd.DataFrame(cur.fetchall())
        # Set the column names to match the table schema
        df.columns = [desc[0] for desc in cur.description]

    # testing 
    # print(df)

    return df


# Get History for user
def analysis_results(email: str, stock: str, run_date: str):
    with db_conn.get_conn().cursor() as cur:
        cur.execute(f"""select distinct positive_article_count, neutral_article_count, negative_article_count, positive_summary, negative_summary
from logging
where email = '{email}'
        and stock = '{stock}'
        and to_date(run_date) = '{run_date}'"""
        )
        # Fetch all the results into a Pandas DataFrame
        df = pd.DataFrame(cur.fetchall())
        # Set the column names to match the table schema
        df.columns = [desc[0] for desc in cur.description]

    # testing 
    # print(df)

    return df


# USER_HISTORY_DASHBOARD
def user_history_dashboard():
    with db_conn.get_conn().cursor() as cur:
        cur.execute(f"""select to_date(signup_date) signup_date, service_plan, count(email) total_users
from users
group by to_date(signup_date), service_plan
order by signup_date desc"""
        )
        # Fetch all the results into a Pandas DataFrame
        df = pd.DataFrame(cur.fetchall())
        # Set the column names to match the table schema
        df.columns = [desc[0] for desc in cur.description]

    return df

# STOCK_HISTORY_DASHBOARD
def stock_history_dashboard():
    with db_conn.get_conn().cursor() as cur:
        cur.execute(f"""select distinct stock, count(distinct to_date(run_date)) overall_runs
from logging
group by stock
order by overall_runs desc"""
        )
        # Fetch all the results into a Pandas DataFrame
        df = pd.DataFrame(cur.fetchall())
        # Set the column names to match the table schema
        df.columns = [desc[0] for desc in cur.description]

    return df


# USAGE_HISTORY_DASHBOARD
def usage_history_dashboard():
    with db_conn.get_conn().cursor() as cur:
        cur.execute(f"""select distinct to_date(run_date) run_date, 
                count(distinct email) unique_users, 
                count(distinct stock) unique_stocks,
                count(distinct email || stock) total_runs
from logging
group by to_date(run_date)
order by to_date(run_date) desc"""
        )
        # Fetch all the results into a Pandas DataFrame
        df = pd.DataFrame(cur.fetchall())
        # Set the column names to match the table schema
        df.columns = [desc[0] for desc in cur.description]

    return df


