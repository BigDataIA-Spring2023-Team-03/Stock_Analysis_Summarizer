import snowflake.connector
from dbutils.pooled_db import PooledDB

# Define your Snowflake connection parameters
conn_params = {
    'account': 'sh13682.ca-central-1.aws',
    'user': 'DAMG7245_SA',
    'password': '<password>',
    'database': 'STOCK_ANALYSIS_APP',
    'schema': 'PUBLIC',
    'warehouse': 'compute_wh',
    'role': 'STOCK_ANALYSIS_APP',
    'client_session_keep_alive': True
}

# Define a function to create Snowflake connections
def create_conn():
    return snowflake.connector.connect(**conn_params)

# Create a Snowflake connection pool
pool = PooledDB(
    creator=create_conn,
    maxconnections=10,  # set the maximum number of connections
    maxcached=5        # set the maximum number of idle connections
)

# Export the connection pool object
def get_conn():
    return pool.connection()