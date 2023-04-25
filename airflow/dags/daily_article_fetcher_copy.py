import boto3
import json
from datetime import datetime, timedelta
import time
import requests
import re
from airflow.models import DAG, XCom, Variable
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy import DummyOperator

import transformers
# Summarization
from transformers import pipeline

# Sentiment
from transformers import AutoTokenizer, AutoModelForSequenceClassification

aws_access_key_id = Variable.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = Variable.get('AWS_SECRET_ACCESS_KEY')
# S3 Details:
s3_bucket_name = 'stock-analysis-summarizer'

run_type = "{{ dag_run.conf['run_type'] }}"

# Create an S3 client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
)

X_RapidAPI_Key = Variable.get('X_RapidAPI_Key')
X_RapidAPI_Host = Variable.get('X_RapidAPI_Host')

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 4, 18),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'daily_article_fetcher_copy',
    default_args=default_args,
    description='Fetches Article from Seeking Alpha that were written since the last run (1 day)',
    schedule_interval=timedelta(days=1),
    params={"run_type": ""}
)

##########################################################################
def check_stock_exists(stock):
    try:
        response = s3_client.list_objects_v2(Bucket=s3_bucket_name, Prefix=stock)
        if 'Contents' in response:
            return True
        else:
            return False
    except Exception as e:
        print(f'Error: {e}')
        return False


def get_latest_date(stock):
    latest_date = None
    try:
        response = s3_client.list_objects_v2(Bucket=s3_bucket_name, Prefix=f'Analysis_Results/{stock}/')
        if 'Contents' in response:
            files = [obj['Key'].split('/')[2] for obj in response['Contents']]
            # List comprehension to extract date string from each file name
            dates = [re.search(r'\d{2}_\d{2}_\d{4}', file_name).group() for file_name in files]
            dates.sort(reverse=True)
            latest_date = dates[0]
    except Exception as e:
        print(f'Error: {e}')
    return latest_date

def get_new_article_data(stock, run):
    url = "https://seeking-alpha.p.rapidapi.com/analysis/v2/list"
    current_timestamp = int(time.time())
    if run == 'init':
        if check_stock_exists(stock):
            latest_date = get_latest_date(stock)
            # Only run once a day
            if latest_date:
                latest_date_timestamp = int(time.mktime(time.strptime(latest_date, '%m-%d-%Y')))
                latest_date_timestamp = latest_date_timestamp + timedelta(days=1)
                time_elapsed = current_timestamp - latest_date_timestamp
        else:
            time_elapsed = current_timestamp - (30 * 24 * 60 * 60)
    else:
        # TODO: check if stock exists
        time_elapsed = current_timestamp - (24 * 60 * 60)

    if time_elapsed > 0:
        querystring = {"id": stock, "since": time_elapsed, "until": current_timestamp}
        headers = {
            "X-RapidAPI-Key": X_RapidAPI_Key,
            "X-RapidAPI-Host": X_RapidAPI_Host
        }
        response = requests.request("GET", url, headers=headers, params=querystring)

        if response.status_code == 204:
            print(f'No New Analysis Articles for {i}')

        # Get Data from the articles
        else:
            # Unique Publish Date List
            unique_publish_date = []

            res = json.loads(response.text)
            article_data = []
            for j in res['data']:
                id = j['id']
                url = "https://seeking-alpha.p.rapidapi.com/analysis/v2/get-details"
                querystring = {"id": id}
                headers = {
                    "X-RapidAPI-Key": X_RapidAPI_Key,
                    "X-RapidAPI-Host": X_RapidAPI_Host
                }
                response = requests.request("GET", url, headers=headers, params=querystring)
                if response.status_code == 200:
                    # print(response.text)
                    res = json.loads(response.text)
                    print(res)

                    # TODO: Convert content from HTML to string
                    # res['data']['attributes']['content']

                    # TODO:
                    # Check if can get article
                    if 'errors' in res:
                        print("The dictionary has a key called 'error'")
                        print(response.text)
                    else:
                        # Append Unique Publish dates --> used in file creation
                        date_obj = datetime.fromisoformat(res['data']['attributes']['publishOn'])

                        new_date_str = date_obj.strftime('%m_%d_%Y')
                        if new_date_str not in unique_publish_date:
                            unique_publish_date.append(new_date_str)

                        # Turn summary from seeking_alpha into one string
                        summary_from_seeking_alpha = res['data']['attributes']['summary']
                        summary_from_seeking_alpha = ' '.join(summary_from_seeking_alpha)

                        # print(res)
                        data = {
                            'article_id': id,
                            'title': res['data']['attributes']['title'],
                            'publish_date': res['data']['attributes']['publishOn'],
                            'summary_from_seeking_alpha': summary_from_seeking_alpha
                            # 'content': res['data']['attributes']['content']
                        }
                        # TESTING
                        print(data)
                        article_data.append(data)
    return article_data, unique_publish_date
    # Push to XCOM
    ti.xcom_push(key=f'{stock}', value=article_data)


# # Testing
# stocks = ['aapl']
# for stock in stocks:
#     article_data = get_new_article_data(stock)


# Get Summary of Content using Facebook BART Large CNN transformer model
def article_summary(article):
    content = article['summary_from_seeking_alpha']
    # # Summarize
    # summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    #
    # summary = summarizer(content, max_length=130, min_length=30, do_sample=False)
    # # [{'summary_text': "Figure 1: A look at the world's tallest man. Figure 2: The tallest woman in the world. Figure 3: The world's largest man in the smallest city."}]
    # summary = summary[0]['summary_text']

    API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    headers = {"Authorization": "Bearer <token>"}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    article = query({
        "inputs": content,
    })

    print(f'Summary created for article: {article}')

    # Push to XCOM
    # ti.xcom_push(key='article', value=summary)

    return article


# # Testing
# article = article_data[0]
# for i, article in enumerate(article_data):
#     # Get Summary
#     # summary = article_summary(article)

#     # Add summary to article dictionary
#     # article_data[i]['bart_summary'] = summary

#     # Get Sentiment
#     probs = get_sentiment(summary)
#     # Add sentiment to article dictionary
#     article_data[i]['finbert_sentiment'] = probs


# Get Sentiment of Summary using FinBERT model from Prosus AI
def get_sentiment(summary):
    API_URL = "https://api-inference.huggingface.co/models/ProsusAI/finbert"
    headers = {"Authorization": "Bearer <token>"}

    response = requests.get(API_URL)
    print(response.status_code)
    while response.status_code == 503:
        time.sleep(5)
        response = requests.get(API_URL)
        print(response.status_code)

    # Make the prediction
    output = requests.post(API_URL, headers=headers, json={"text": summary[0]['summary_text']}).json()

    print(f'Sentiment derived for the article')
    print('output', output)
    print([i['score'] for i in output])

    # convert to list
    return [i['score'] for i in output]


# Push Results to S3
def push_summarized_data(stock, date, article_data):
    # TESTING
    print(article_data)

    # DONT NEED - Convert the list of dictionaries to a JSON string
    json_data = json.dumps(article_data, indent=4, default=str)
    # TESTING
    print(json_data)

    # %Y-%m-%d %H:%M:%S
    # current_time = datetime.datetime.now().strftime("%Y_%m_%d")
    # print(current_time)
    file_name = f'Analysis_Results/{stock}/{stock}_{date}.json'

    # Upload the JSON string to S3
    s3_client.put_object(Bucket=s3_bucket_name, Key=file_name, Body=json_data)

    print(f'{file_name} Uploaded to S3')


###################################################################################################
# One Main Function as a Task
def main(**kwargs):
    input_stocks = kwargs['stocks']
    run_type = kwargs['run_type']
    for stock in stocks:
        # try:
        print(f'Stock: {stock}')
        start_time = time.time()

        article_data, unique_publish_date = get_new_article_data(stock, run_type)

        article_data_date_subset = []
        for j,date in enumerate(unique_publish_date):
            # for each article
            for i, article in enumerate(article_data):
                # Check if the dates line up
                if date == datetime.fromisoformat(article['publish_date']).strftime('%m_%d_%Y'):
                    # print(date)
                    # print(article['publish_date'])

                    # Get Summary
                    summary = article_summary(article)
                    # Add summary to article dictionary
                    article_data[i]['bart_summary'] = summary
                    # Get Sentiment
                    probs = get_sentiment(summary)
                    # Add sentiment to article dictionary
                    article_data[i]['sentiment'] = probs

                    # Append
                    article_data_date_subset.append(article_data[i])

            # Push Data to S3
            push_summarized_data(stock, date, article_data_date_subset)
            # print('done')
        # except Exception as e:
        #     print(f'Error during processing for {stock}')
        #     print(str(e))

        print(f"Time to complete: {(time.time() - start_time)} seconds")


###################################################################################################
# TASKS:
# testing = PythonOperator(
#     task_id='testing',
#     python_callable=testing,
#     provide_context=True,
#     dag=dag
# )

# TESTING
stocks = ['amzn']
# TOP 10 stocks in SP500 by index weight:
# stocks = ['AAPL', 'MSFT', 'AMZN', 'NVDA', 'GOOGL', 'BRK.B', 'GOOG', 'TSLA', 'UNH', 'META']

main = PythonOperator(
    task_id='main',
    provide_context=True,
    python_callable=main,
    op_kwargs={'stocks': stocks, 'run_type': run_type},
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