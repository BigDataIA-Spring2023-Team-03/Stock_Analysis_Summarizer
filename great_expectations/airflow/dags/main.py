from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
import snowflake.connector
import pandas as pd
import os
from sqlalchemy import create_engine
from great_expectations_provider.operators.great_expectations import GreatExpectationsOperator
from great_expectations.data_context.types.base import (
    DataContextConfig,
    CheckpointConfig
)

base_path = "/opt/airflow/working_dir"
data_dir = os.path.join(base_path, "News-Aggregator", "great_expectations", "data")
ge_root_dir = os.path.join(base_path, "great_expectations")
report_dir = os.path.join(ge_root_dir, "uncommitted/data_docs/local_site/validations/nyt_raw_data_suite" )


def delete_file(delete_file_path):
    os.remove(delete_file_path)

# Snowflake connection parameters
conn = {
    'account': 'sh13682.ca-central-1.aws',
    'user': 'DAMG7245_SA',
    'password': 'DAMG7245_final',
    'database': 'STOCK_ANALYSIS_APP',
    'schema': 'PUBLIC',
    'warehouse': 'compute_wh',
    'role': 'STOCK_ANALYSIS_APP',
    'client_session_keep_alive': True
}

# Define the file path where you want to save the CSV file
file_path = '/opt/airflow/working_dir/data/logging.csv'

# Execute SQL query and store results in a CSV file
sql_query = "SELECT * FROM logging"

def get_data(conn, sql_query, file_path):
    # Establish a connection to Snowflake
    connection = snowflake.connector.connect(**conn)
    # Execute SQL query and store results in a DataFrame
    df = pd.read_sql(sql_query, connection)
    # Store the DataFrame as a CSV file at the specified file path
    df.to_csv(file_path, index=False)
    # Closing the connection
    connection.close()


dag = DAG(
    dag_id="stock_analyzer",
    schedule="0 0 * * *",   # https://crontab.guru/
    start_date=days_ago(0),
    catchup=False,
    dagrun_timeout=timedelta(minutes=60),
    tags=["labs", "damg7245"],
)

with dag:

    stocks_data_validation = GreatExpectationsOperator(
        task_id="stocks_data_validation",
        data_context_root_dir=ge_root_dir,
        checkpoint_name="logging_v1",
        fail_task_on_validation_failure=False
    )

    delete_file_task = PythonOperator(
    task_id='delete_existing_file',
    python_callable=delete_file,
    op_kwargs={'delete_file_path': '/opt/airflow/working_dir/data/logging.csv'},
    dag=dag
    )

    get_data_task = PythonOperator(   
    task_id='get_data',
    python_callable = get_data,
    op_kwargs={
            'conn': conn,
            'sql_query': sql_query,
            'file_path': file_path
        }
    )

    # Flow
    delete_file_task >> get_data_task >> stocks_data_validation 

