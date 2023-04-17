import boto3
import io
import json
import os
from datetime import datetime, timedelta
from airflow.models import DAG, XCom, Variable
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.models.param import Param

# Summarization
from transformers import pipeline

# Sentiment
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# import openai

aws_access_key_id = Variable.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = Variable.get('AWS_SECRET_ACCESS_KEY')
s3_bucket_name = 'stock-analysis-summarizer'

whisper_secret_key = Variable.get('WHISPER_API_SECRET')

# openai.api_key = whisper_secret_key

# PARAMS --> from Streamlit
# user_input = {
#     "filename": Param('No File Name!', type='string')
# }


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 3, 23),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'daily_article_fetcher',
    default_args=default_args,
    description='Fetches Article from Seeking Alpha that were written since the last run (1 day)',
    schedule_interval=timedelta(days=1),
    # params=user_input
)

# TESTING
# def testing(**kwargs):
#     print(f'Current Working Directory: {os.getcwd()}')
#     print(f"File Input from Streamlit: {kwargs['dag_run'].conf['filename']}")



# TOP 10 stocks in SP500 by index weight:
stocks = ['AAPL', 'MSFT', 'AMZN', 'NVDA', 'GOOGL', 'BRK.B', 'GOOG', 'TSLA', 'UNH', 'META']

def get_new_article_data(stock):
    # Get Articles for Stock
    url = "https://seeking-alpha.p.rapidapi.com/analysis/v2/list"
    current_timestamp = int(time.time())
    one_day_ago_timestamp = current_timestamp - (1 * 24 * 60 * 60)

    querystring = {"id": stock,"since": one_month_ago_timestamp ,"until":current_timestamp}
    headers = {
        "X-RapidAPI-Key": "5009248b8amsh32c9cc4b342a2dbp106cb1jsnb3385ef745f8",
        "X-RapidAPI-Host": "seeking-alpha.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)

    if response.status_code == 204:
        print(f'No New Analysis Articles for {i}')
    # Get Data from the articles
    else:
        res = json.loads(response.text)
        article_data = []
        for j in res['data']:
            id = j['id']
            url = "https://seeking-alpha.p.rapidapi.com/analysis/v2/get-details"
            querystring = {"id": id}
            headers = {
                "X-RapidAPI-Key": "5009248b8amsh32c9cc4b342a2dbp106cb1jsnb3385ef745f8",
                "X-RapidAPI-Host": "seeking-alpha.p.rapidapi.com"
            }
            response = requests.request("GET", url, headers=headers, params=querystring)
            if response.status_code == 200:
            # print(response.text)
                res = json.loads(response.text)

                # TODO: Convert content from HTML to string
                # res['data']['attributes']['content']

                # print(res)
                data = {
                    'title': res['data']['attributes']['title'],
                    'summary': res['data']['attributes']['summary'],
                    'content': res['data']['attributes']['content']
                }
                # print(id + ':::: ' + str(data))
                article_data.append(data)
    # return article_data
    # Push to XCOM
    ti.xcom_push(key=stock, value=article_data)


# For each stock do the following
# Get Summary of Content using Facebook BART Large CNN transformer model
def article_summary(ti):
    # Grab Article Data from XCOM
    content = ti.xcom_pull(task_ids=['get_new_article_data'], key=stock)[0]['content']

    # Summarize
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    summary = summarizer(ARTICLE, max_length=130, min_length=30, do_sample=False)

    print(summary)

    # Push to XCOM
    ti.xcom_push(key='article', value=summary)

    pass

# Get Sentiment of Summary using FinBERT model from Prosus AI
def get_sentiment(ti):
    # Grab Summarized Content from XCOM
    summary = ti.xcom_pull(task_ids=['article_summary'], key='article')[0]

    # Get Sentiment
    # num_labels = 3 --> positive, neutral, and negative
    tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
    model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert", num_labels=3)

    # Tokenize the summary
    encoded_text = tokenizer.encode_plus(summary, return_tensors='pt')

    # Pass envoded input into the model to get the predicted sentiment
    logits = model.forward(encoded_text['input_ids'], encoded_text['attention_mask']).logits
    probs = logits.softmax(dim=1)

    # 
    print(probs)

    pass


# Push Results to S3
def push_summarized_data():
    pass


def clear_xcoms(**context):
    # TODO: implement this and call at the end of the dag execution
    pass


###################################################################################################
# TASKS:
# testing = PythonOperator(
#     task_id='testing',
#     python_callable=testing,
#     provide_context=True,
#     dag=dag
# )

get_new_article_data = PythonOperator(
    task_id='get_new_article_data',
    provide_context=True,
    python_callable=get_new_article_data,
    dag=dag
)

article_summary = PythonOperator(
    task_id='article_summary',
    provide_context=True,
    python_callable=article_summary,
    dag=dag
)

get_sentiment = PythonOperator(
    task_id='get_sentiment',
    provide_context=True,
    python_callable=get_sentiment,
    dag=dag
)

push_summarized_data = PythonOperator(
    task_id='push_summarized_data',
    provide_context=True,
    python_callable=push_summarized_data,
    dag=dag
)

# clear_xcoms = PythonOperator(
#     task_id='clear_xcoms',
#     python_callable=clear_xcoms,
#     provide_context=True,
#     dag=dag
# )

start = DummyOperator(
    task_id='start',
    dag=dag
)

end = DummyOperator(
    task_id='end',
    dag=dag
)


###################################################################################################

start >> check_for_new_articles >> article_summary >> get_sentiment >> push_summarized_data >> end 

# start >> process_audio_files >> [push_text, default_quessionaire]
# default_quessionaire >> push_answers
# push_text >> end
# push_answers >> end