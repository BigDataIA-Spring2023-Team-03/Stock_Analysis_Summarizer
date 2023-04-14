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


for item in financial_news['feed']:
    # Access the desired fields within each object
    title = item['title']
    summary = item['summary']
    banner_image = item['banner_image']
    overall_sentiment_score = item['overall_sentiment_score']
    overall_sentiment_label = item['overall_sentiment_label']
    ticker_sentiment = item['ticker_sentiment']

    # Print out the values of the fields
    st.subheader(f'Summary: {title}')
    st.image(banner_image)
    st.text(f'Summary: {summary}')
    st.text(f'Overall Sentiment Score: {overall_sentiment_score}')
    st.text(f'Overall Sentiment Label: {overall_sentiment_label}')
    st.text(f'Ticker Sentiment: {ticker_sentiment}')
    st.text("")
    st.text("")

finance_news = news_api_call(news_api_key)
st.title("News API:")
for article in finance_news:
    st.write(article["title"])
    st.text("")