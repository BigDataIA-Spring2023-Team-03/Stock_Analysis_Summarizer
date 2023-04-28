# Stock Analysis Summarizer
[![FastAPI Unit Tests](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/actions/workflows/pytest.yml/badge.svg)](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/actions/workflows/pytest.yml)

# Code Coverage - CodeCov
<img src="https://codecov.io/gh/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/branch/main/graphs/sunburst.svg?token=NGU9K01WWF" alt="Code Coverage" width="200" height="200">

[![Code Coverage](https://codecov.io/gh/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/branch/main/graph/badge.svg?token=NGU9K01WWF)](https://codecov.io/gh/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer)



# CLaaT Document
https://codelabs-preview.appspot.com/?file_id=1xpThxuUEYJ5D3UqJBafAID6McqWWZlaih32qt9NzPEA#14

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

# Directory Structure
Sentiment_Stock_Forecaster/
┣ .github/
┃ ┗ workflows/
┃   ┗ pytest.yml
┣ Snowflake_SQL/
┃ ┗ create_statements.sql
┣ airflow/
┃ ┣ dags/
┃ ┃ ┣ daily_article_fetcher.py
┃ ┃ ┣ daily_article_fetcher_copy.py
┃ ┃ ┗ new_stock_article_fetcher.py
┃ ┗ docker-compose.yaml
┣ fastapi/
┃ ┣ Authentication/
┃ ┃ ┣ __pycache__/
┃ ┃ ┃ ┣ __init__.cpython-311.pyc
┃ ┃ ┃ ┣ auth.cpython-311.pyc
┃ ┃ ┃ ┗ auth_bearer.cpython-311.pyc
┃ ┃ ┣ __init__.py
┃ ┃ ┣ auth.py
┃ ┃ ┗ auth_bearer.py
┃ ┣ Util/
┃ ┃ ┣ __pycache__/
┃ ┃ ┃ ┣ __init__.cpython-311.pyc
┃ ┃ ┃ ┣ db_conn.cpython-311.pyc
┃ ┃ ┃ ┗ db_util.cpython-311.pyc
┃ ┃ ┣ __init__.py
┃ ┃ ┣ db_conn.py
┃ ┃ ┗ db_util.py
┃ ┣ __pycache__/
┃ ┃ ┣ apis.cpython-311.pyc
┃ ┃ ┗ schemas.cpython-311.pyc
┃ ┣ Dockerfile
┃ ┣ apis.py
┃ ┣ requirements.txt
┃ ┣ schemas.py
┃ ┗ test_apis.py
┣ streamlit/
┃ ┣ .test/
┃ ┃ ┣ include/
┃ ┃ ┃ ┗ python3.11/
┃ ┃ ┗ lib/
┃ ┃   ┗ python3.11/
┃ ┃ ┃   ┗ site-packages/
┃ ┣ Util/
┃ ┃ ┣ __pycache__/
┃ ┃ ┃ ┣ __init__.cpython-311.pyc
┃ ┃ ┃ ┣ db_conn.cpython-311.pyc
┃ ┃ ┃ ┗ db_util.cpython-311.pyc
┃ ┃ ┣ .env
┃ ┃ ┣ __init__.py
┃ ┃ ┣ db_conn.py
┃ ┃ ┗ db_util.py
┃ ┣ components/
┃ ┃ ┣ __pycache__/
┃ ┃ ┃ ┣ admin_dashboard.cpython-311.pyc
┃ ┃ ┃ ┣ analysis_vs_reality.cpython-311.pyc
┃ ┃ ┃ ┣ login.cpython-311.pyc
┃ ┃ ┃ ┣ portfolio_uploader.cpython-311.pyc
┃ ┃ ┃ ┣ register.cpython-311.pyc
┃ ┃ ┃ ┗ upgrade_plan.cpython-311.pyc
┃ ┃ ┣ admin_dashboard.py
┃ ┃ ┣ analysis_vs_reality.py
┃ ┃ ┣ login.py
┃ ┃ ┣ portfolio_uploader.py
┃ ┃ ┣ register.py
┃ ┃ ┗ upgrade_plan.py
┃ ┣ scrap/
┃ ┃ ┣ abc.py
┃ ┃ ┣ newspage.py
┃ ┃ ┣ scraper.py
┃ ┃ ┗ userinfo.db
┃ ┣ Dockerfile
┃ ┣ Home.py
┃ ┣ Welcome.py
┃ ┣ analysis_pipeline.py
┃ ┣ example_format.json
┃ ┗ requirements.txt
┣ .env
┣ .gitignore
┣ README.md
┣ arch.py
┣ docker-compose.yml
┗ stock_analysis_summarizer



