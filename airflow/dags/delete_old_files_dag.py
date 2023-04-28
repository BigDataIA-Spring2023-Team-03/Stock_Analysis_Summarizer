import boto3
# from decouple import config
import re
from datetime import datetime, timedelta
from airflow.models import DAG, Variable
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy import DummyOperator

# AWS KEYS
aws_access_key_id = Variable.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = Variable.get('AWS_SECRET_ACCESS_KEY')
# S3 Details:
s3_bucket_name = 'stock-analysis-summarizer'

# Create an S3 client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 4, 18),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'delete_old_files',
    default_args=default_args,
    description='Deletes Analysis Files that are more than 30 days old',
    schedule_interval=timedelta(days=1)
)

# TESTING
# def testing(**kwargs):
#     print(f'Current Working Directory: {os.getcwd()}')
#     print(f"File Input from Streamlit: {kwargs['dag_run'].conf['filename']}")


##########################################################################
def get_filenames_from_s3():
    # List all files in S3 bucket
    file_list = []
    try:
        response = s3_client.list_objects_v2(Bucket=s3_bucket_name)
        for obj in response['Contents']:
            print(obj['Key'])
            file_list.append(obj['Key'])
    except Exception as e:
        print(f"An error occurred while listing files: {e}")

    print(f'Total Files in bucket: {len(file_list)}')
    return file_list


def pull_date_from_file(filename):
    # Extracting date components from the filename using regex
    match = re.search(r"_(\d{2})_(\d{2})_(\d{4}).json", filename)

    # Creating a datetime object from extracted date components
    if match:

        month = int(match.group(1))
        day = int(match.group(2))
        year = int(match.group(3))
        date_obj = datetime(year, month, day)
        # print(date_obj)

        # Check if more than 30 days old
        delta = datetime.now() - date_obj
        if delta.days > 30:
            print("The date is more than 30 days old.")
            return True
        # else:
        #     print("The date is within the last 30 days.")
        #     return False
    else:
        print("Invalid filename format.")


def delete_from_s3(filename):
    # Deleting file from S3 bucket
    try:
        s3_client.delete_object(Bucket=s3_bucket_name, Key=filename)
        print(f"The file '{filename}' has been deleted from S3")
    except Exception as e:
        print(f"An error occurred while deleting the file: {e}")


# TEST
# filename = "meta_03_27_2023.json"
# pull_date_from_file(filename)

# file_list = ["meta_03_20_2023.json", "meta_03_22_2023.json", "meta_04_26_2023.json", "meta_04_27_2023.json"]
file_list = get_filenames_from_s3()
files_deleted = 0
# Loop through all files and delete files with data from more than 30 days
for filename in file_list:
    if pull_date_from_file(filename):
        print(filename)
        # delete file from S3
        # delete_from_s3(filename)
        files_deleted += 1

print(f'{files_deleted} files deleted')

###################################################################################################
# One Main Function as a Task
def main():
    file_list = get_filenames_from_s3()
    files_deleted = 0
    # Loop through all files and delete files with data from more than 30 days
    for filename in file_list:
        if pull_date_from_file(filename):
            print(filename)
            # delete file from S3
            delete_from_s3(filename)
            files_deleted += 1

    print(f'{files_deleted} files deleted')


###################################################################################################
# TASKS:
main = PythonOperator(
    task_id='main',
    provide_context=True,
    python_callable=main,
    dag=dag
)

start = DummyOperator(
    task_id='start',
    dag=dag
)

end = DummyOperator(
    task_id='end',
    dag=dag
)

###################################################################################################

start >> main >> end

###################################################################################################