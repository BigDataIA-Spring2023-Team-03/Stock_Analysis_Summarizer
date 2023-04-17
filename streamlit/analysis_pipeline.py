import boto3
import requests
import time
import datetime
import json
from decouple import config

# Summarization
from transformers import pipeline

# Sentiment
from transformers import AutoTokenizer, AutoModelForSequenceClassification


# AWS KEYS
aws_access_key_id = config('aws_access_key_id')
aws_secret_access_key = config('aws_secret_access_key')

# RapidAPI Keys
X_RapidAPI_Key = config('X-RapidAPI-Key')
X_RapidAPI_Host = config('X-RapidAPI-Host')

# S3 Details:
s3_bucket_name = 'stock-analysis-summarizer'

# Create an S3 client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
)

##########################################################################



# TOP 10 stocks in SP500 by index weight:
# stocks = ['AAPL', 'MSFT', 'AMZN', 'NVDA', 'GOOGL', 'BRK.B', 'GOOG', 'TSLA', 'UNH', 'META']

def get_new_article_data(stock):
    # Get Articles for Stock
    url = "https://seeking-alpha.p.rapidapi.com/analysis/v2/list"
    current_timestamp = int(time.time())
    one_day_ago_timestamp = current_timestamp - (7 * 24 * 60 * 60)

    querystring = {"id": stock,"since": one_day_ago_timestamp ,"until":current_timestamp}
    headers = {
        "X-RapidAPI-Key": X_RapidAPI_Key,
        "X-RapidAPI-Host": X_RapidAPI_Host
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
                "X-RapidAPI-Key": X_RapidAPI_Key,
                "X-RapidAPI-Host": X_RapidAPI_Host
            }
            response = requests.request("GET", url, headers=headers, params=querystring)
            if response.status_code == 200:
            # print(response.text)
                res = json.loads(response.text)

                # TODO: Convert content from HTML to string
                # res['data']['attributes']['content']

                # print(res)
                data = {
                    'article_id': id,
                    'title': res['data']['attributes']['title'],
                    'publish_date': res['data']['attributes']['publishOn'],
                    'summary_from_seeking_alpha': res['data']['attributes']['summary'],
                    'content': res['data']['attributes']['content']
                }
                # print(id + ':::: ' + str(data))
                article_data.append(data)
    return article_data
    # Push to XCOM
    # ti.xcom_push(key=stock, value=article_data)
    
# Testing
stocks = ['aapl']
for stock in stocks:
    article_data = get_new_article_data(stock)
    


# Get Summary of Content using Facebook BART Large CNN transformer model
def article_summary(article):
    # Grab Article Data from XCOM
    # content = ti.xcom_pull(task_ids=['get_new_article_data'], key=filename)[0]['text']
    
    # first 100 characters due to size error
    # Token indices sequence length is longer than the specified maximum sequence length for this model (4191 > 1024). Running this sequence through the model will result in indexing errors
    content = article['content'][0:100]
    
    # Summarize
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    summary = summarizer(content, max_length=130, min_length=30, do_sample=False)
    # [{'summary_text': "Figure 1: A look at the world's tallest man. Figure 2: The tallest woman in the world. Figure 3: The world's largest man in the smallest city."}]
    summary = summary[0]['summary_text']

    print(f'Summary created for article: {article}')
    
    # Push to XCOM
    # ti.xcom_push(key='article', value=summary)
    
    return summary

# Testing
article = article_data[0]
for i, article in enumerate(article_data):
    # Get Summary
    # summary = article_summary(article)
    
    # Add summary to article dictionary
    # article_data[i]['bart_summary'] = summary
    
    # Get Sentiment
    probs = get_sentiment(summary)
    # Add sentiment to article dictionary
    article_data[i]['finbert_sentiment'] = probs
    
    


# Get Sentiment of Summary using FinBERT model from Prosus AI
def get_sentiment(summary):
    # Grab Summarized Content from XCOM
    # summary = ti.xcom_pull(task_ids=['article_summary'], key='article')[0]
    
    # Get Sentiment
    # num_labels = 3 --> positive, negative, neutral
    tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
    model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert", num_labels=3)
    
    # Tokenize the summary
    encoded_text = tokenizer.encode_plus(summary, return_tensors='pt')
    
    # Pass encoded input into the model to get the predicted sentiment
    logits = model.forward(encoded_text['input_ids'], encoded_text['attention_mask']).logits
    probs = logits.softmax(dim=1)

    # Parse out predicted probabilities
    probs = probs.detach().numpy()[0]  # convert to numpy array and retrieve first element (since we only have one input text)
    positive_prob = probs[0]  # probability for positive sentiment
    negative_prob = probs[1]  # probability for negative sentiment
    neutral_prob = probs[2]  # probability for neutral sentiment

    print(f'Sentiment derived for the article')
    print(probs)
    
    # convert to list
    return list(probs)




# Push Results to S3
def push_summarized_data(stock, article_data):
    # Convert the list of dictionaries to a JSON string
    json_data = json.dumps(str(article_data))
    
    # %Y-%m-%d %H:%M:%S
    current_time = datetime.datetime.now().strftime("%Y_%m_%d")
    # print(current_time)
    file_name = f'Analysis_Results/{stock}_{current_time}.json'
    
    # Upload the JSON string to S3
    s3_client.put_object(Bucket=s3_bucket_name, Key=file_name, Body=json_data)
    
    print(f'{file_name} Uploaded to S3')
    
# TESTING
push_summarized_data(stock, article_data)


if __name__=='__main__':
    # TOP 10 stocks in SP500 by index weight:
    # stocks = ['AAPL', 'MSFT', 'AMZN', 'NVDA', 'GOOGL', 'BRK.B', 'GOOG', 'TSLA', 'UNH', 'META']
    stocks = ['aapl']
    # For each stock
    for stock in stocks:
        print(f'Stock: {stock}')
        start_time = time.time()

        article_data = get_new_article_data(stock)
        
        # for each article
        for i, article in enumerate(article_data):
            # Get Summary
            summary = article_summary(article)
            
            # Add summary to article dictionary
            article_data[i]['bart_summary'] = summary
            
            # Get Sentiment
            probs = get_sentiment(summary)
            # Add sentiment to article dictionary
            article_data[i]['sentiment'] = probs
            
        # Push Data to S3
        push_summarized_data(stock, article_data)
        
        print(f"Time to complete: {(time.time() - start_time)} seconds")
        
        
        
# SCRAP
# article_data['sentiment'].tolist()
