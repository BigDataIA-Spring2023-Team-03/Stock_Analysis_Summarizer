# Stock Analysis Summarizer
[![FastAPI Unit Tests](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/actions/workflows/pytest.yml/badge.svg?branch=main&event=push)](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/actions/workflows/pytest.yml)

# CLaaT Document
https://docs.google.com/document/d/12P7LfVvkH8Tvr3W56wv3sN52bWdVNFJHefoswlgemzQ/edit#

# Google Document
https://docs.google.com/document/d/1p_WCcLuuckm8ZOMLAS3dW51qS42W7ai5eQi7n4rgSek/edit

# Overview

This project aims to provide summary of the analysis articles for a given portfolio of stock tickers. The data is collected from SeekingAlpha, a financial news website that publishes analysis articles on various stocks.

# Technologies Used
![Python](https://img.shields.io/badge/python-grey?style=for-the-badge&logo=python&logoColor=ffdd54)
![](https://img.shields.io/badge/FastAPI-4285F4?style=for-the-badge&logo=fastapi&logoColor=white)
![](https://img.shields.io/badge/SeekingAlpha-orange?style=for-the-badge&logo=seeking-alpha&logoColor=white)
![](https://img.shields.io/badge/GitHub_Actions-green?style=for-the-badge&logo=github-actions&logoColor=white)
![](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![](https://img.shields.io/badge/Snowflake-blue?style=for-the-badge&logo=Snowflake&logoColor=white)

# Workflow
- User enters a portfolio of stock tickers in the Streamlit web interface.
- The Airflow DAG is triggered to collect articles related to the provided stock tickers from SeekingAlpha.
- The collected articles are preprocessed using NLP techniques, and sentiment analysis is performed on each article.
- The results are stored in the database.
- Two summaries are generated from the sentiment analysis results: one for all positive articles and another for all negative articles.
- The summaries are displayed in the Streamlit web interface.
- TODO: add more




