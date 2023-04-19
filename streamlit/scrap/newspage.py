import streamlit as st
from scraper import news_api_call, alpha_vantage_api_call
from dotenv import load_dotenv
import os
import json

load_dotenv()

news_api_key = os.getenv("NEWS_API")
alpha_vantage_api_key = os.getenv("ALPHA_VANTAGE_API")

financial_news = alpha_vantage_api_call(alpha_vantage_api_key)
st.title("Alpha Vantage  news:")
st.text(financial_news)

col1, col2 = st.columns([5, 5])

count = 0
# Loop through the items in the feed
for item in financial_news['feed']:
    # Access the desired fields within each object
    title = item['title']
    summary = item['summary']
    banner_image = item['banner_image']
    overall_sentiment_score = item['overall_sentiment_score']
    overall_sentiment_label = item['overall_sentiment_label']
    ticker_sentiment = item['ticker_sentiment']
    

    # Display the item in the columns
    if count%2==0:
        with col1:
            st.subheader(title)
            st.image(banner_image)
            st.text(f'Summary: {summary}')
            st.text(f'Overall Sentiment Score: {overall_sentiment_score}')
            st.text(f'Overall Sentiment Label: {overall_sentiment_label}')
            st.text(f'Ticker Sentiment: {ticker_sentiment}')
            st.markdown("""---""")
            st.text("")
    else:
        with col2:
            st.subheader(title)
            st.image(banner_image)
            st.text(f'Summary: {summary}')
            st.text(f'Overall Sentiment Score: {overall_sentiment_score}')
            st.text(f'Overall Sentiment Label: {overall_sentiment_label}')
            st.text(f'Ticker Sentiment: {ticker_sentiment}')
            st.markdown("""---""")
            st.text("")
    count+=1

finance_news = news_api_call(news_api_key)
st.title("News API:")
for article in finance_news:
    st.write(article["title"])
    st.text("")