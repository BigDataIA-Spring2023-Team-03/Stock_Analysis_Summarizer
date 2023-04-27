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

* [.github/](./Sentiment_Stock_Forecaster/.github)
  * [workflows/](./Sentiment_Stock_Forecaster/.github/workflows)
    * [pytest.yml](./Sentiment_Stock_Forecaster/.github/workflows/pytest.yml)
* [Snowflake_SQL/](./Sentiment_Stock_Forecaster/Snowflake_SQL)
  * [create_statements.sql](./Sentiment_Stock_Forecaster/Snowflake_SQL/create_statements.sql)
* [airflow/](./Sentiment_Stock_Forecaster/airflow)
  * [dags/](./Sentiment_Stock_Forecaster/airflow/dags)
    * [daily_article_fetcher.py](./Sentiment_Stock_Forecaster/airflow/dags/daily_article_fetcher.py)
    * [daily_article_fetcher_copy.py](./Sentiment_Stock_Forecaster/airflow/dags/daily_article_fetcher_copy.py)
    * [new_stock_article_fetcher.py](./Sentiment_Stock_Forecaster/airflow/dags/new_stock_article_fetcher.py)
  * [docker-compose.yaml](./Sentiment_Stock_Forecaster/airflow/docker-compose.yaml)
* [dataset/](./Sentiment_Stock_Forecaster/dataset)
  * [faang_stocks.xlsx](./Sentiment_Stock_Forecaster/dataset/faang_stocks.xlsx)
  * [ticker.xlsx](./Sentiment_Stock_Forecaster/dataset/ticker.xlsx)
* [fastapi/](./Sentiment_Stock_Forecaster/fastapi)
  * [Authentication/](./Sentiment_Stock_Forecaster/fastapi/Authentication)
    * [__init__.py](./Sentiment_Stock_Forecaster/fastapi/Authentication/__init__.py)
    * [auth.py](./Sentiment_Stock_Forecaster/fastapi/Authentication/auth.py)
    * [auth_bearer.py](./Sentiment_Stock_Forecaster/fastapi/Authentication/auth_bearer.py)
  * [Util/](./Sentiment_Stock_Forecaster/fastapi/Util)
    * [__init__.py](./Sentiment_Stock_Forecaster/fastapi/Util/__init__.py)
    * [db_conn.py](./Sentiment_Stock_Forecaster/fastapi/Util/db_conn.py)
    * [db_util.py](./Sentiment_Stock_Forecaster/fastapi/Util/db_util.py)
  * [fastapi_env/](./Sentiment_Stock_Forecaster/fastapi/fastapi_env)
    * [bin/](./Sentiment_Stock_Forecaster/fastapi/fastapi_env/bin)
      * [Activate.ps1](./Sentiment_Stock_Forecaster/fastapi/fastapi_env/bin/Activate.ps1)
      * [activate](./Sentiment_Stock_Forecaster/fastapi/fastapi_env/bin/activate)
      * [activate.csh](./Sentiment_Stock_Forecaster/fastapi/fastapi_env/bin/activate.csh)
      * [activate.fish](./Sentiment_Stock_Forecaster/fastapi/fastapi_env/bin/activate.fish)
      * [email_validator](./Sentiment_Stock_Forecaster/fastapi/fastapi_env/bin/email_validator)
      * [normalizer](./Sentiment_Stock_Forecaster/fastapi/fastapi_env/bin/normalizer)
      * [pip](./Sentiment_Stock_Forecaster/fastapi/fastapi_env/bin/pip)
      * [pip3](./Sentiment_Stock_Forecaster/fastapi/fastapi_env/bin/pip3)
      * [pip3.10](./Sentiment_Stock_Forecaster/fastapi/fastapi_env/bin/pip3.10)
      * [python](./Sentiment_Stock_Forecaster/fastapi/fastapi_env/bin/python)
      * [python3](./Sentiment_Stock_Forecaster/fastapi/fastapi_env/bin/python3)
      * [python3.10](./Sentiment_Stock_Forecaster/fastapi/fastapi_env/bin/python3.10)
      * [snowflake-dump-certs](./Sentiment_Stock_Forecaster/fastapi/fastapi_env/bin/snowflake-dump-certs)
      * [snowflake-dump-ocsp-response](./Sentiment_Stock_Forecaster/fastapi/fastapi_env/bin/snowflake-dump-ocsp-response)
      * [snowflake-dump-ocsp-response-cache](./Sentiment_Stock_Forecaster/fastapi/fastapi_env/bin/snowflake-dump-ocsp-response-cache)
      * [snowflake-export-certs](./Sentiment_Stock_Forecaster/fastapi/fastapi_env/bin/snowflake-export-certs)
      * [uvicorn](./Sentiment_Stock_Forecaster/fastapi/fastapi_env/bin/uvicorn)
    * [lib/](./Sentiment_Stock_Forecaster/fastapi/fastapi_env/lib)
      * [python3.10/](./Sentiment_Stock_Forecaster/fastapi/fastapi_env/lib/python3.10)
        * [site-packages/](./Sentiment_Stock_Forecaster/fastapi/fastapi_env/lib/python3.10/site-packages)
    * [lib64/](./Sentiment_Stock_Forecaster/fastapi/fastapi_env/lib64)
      * [python3.10/](./Sentiment_Stock_Forecaster/fastapi/fastapi_env/lib64/python3.10)
        * [site-packages/](./Sentiment_Stock_Forecaster/fastapi/fastapi_env/lib64/python3.10/site-packages)
    * [pyvenv.cfg](./Sentiment_Stock_Forecaster/fastapi/fastapi_env/pyvenv.cfg)
  * [apis.py](./Sentiment_Stock_Forecaster/fastapi/apis.py)
  * [requirements.txt](./Sentiment_Stock_Forecaster/fastapi/requirements.txt)
  * [schemas.py](./Sentiment_Stock_Forecaster/fastapi/schemas.py)
  * [test_apis.py](./Sentiment_Stock_Forecaster/fastapi/test_apis.py)
* [streamlit/](./Sentiment_Stock_Forecaster/streamlit)
  * [.test/](./Sentiment_Stock_Forecaster/streamlit/.test)
    * [include/](./Sentiment_Stock_Forecaster/streamlit/.test/include)
      * [python3.11/](./Sentiment_Stock_Forecaster/streamlit/.test/include/python3.11)
    * [lib/](./Sentiment_Stock_Forecaster/streamlit/.test/lib)
      * [python3.11/](./Sentiment_Stock_Forecaster/streamlit/.test/lib/python3.11)
        * [site-packages/](./Sentiment_Stock_Forecaster/streamlit/.test/lib/python3.11/site-packages)
  * [Util/](./Sentiment_Stock_Forecaster/streamlit/Util)
    * [__pycache__/](./Sentiment_Stock_Forecaster/streamlit/Util/__pycache__)
      * [__init__.cpython-311.pyc](./Sentiment_Stock_Forecaster/streamlit/Util/__pycache__/__init__.cpython-311.pyc)
      * [db_conn.cpython-311.pyc](./Sentiment_Stock_Forecaster/streamlit/Util/__pycache__/db_conn.cpython-311.pyc)
      * [db_util.cpython-311.pyc](./Sentiment_Stock_Forecaster/streamlit/Util/__pycache__/db_util.cpython-311.pyc)
    * [__init__.py](./Sentiment_Stock_Forecaster/streamlit/Util/__init__.py)
    * [db_conn.py](./Sentiment_Stock_Forecaster/streamlit/Util/db_conn.py)
    * [db_util.py](./Sentiment_Stock_Forecaster/streamlit/Util/db_util.py)
  * [components/](./Sentiment_Stock_Forecaster/streamlit/components)
    * [__pycache__/](./Sentiment_Stock_Forecaster/streamlit/components/__pycache__)
      * [login.cpython-311.pyc](./Sentiment_Stock_Forecaster/streamlit/components/__pycache__/login.cpython-311.pyc)
      * [portfolio_uploader.cpython-311.pyc](./Sentiment_Stock_Forecaster/streamlit/components/__pycache__/portfolio_uploader.cpython-311.pyc)
      * [register.cpython-311.pyc](./Sentiment_Stock_Forecaster/streamlit/components/__pycache__/register.cpython-311.pyc)
    * [admin_dashboard.py](./Sentiment_Stock_Forecaster/streamlit/components/admin_dashboard.py)
    * [analysis_vs_reality.py](./Sentiment_Stock_Forecaster/streamlit/components/analysis_vs_reality.py)
    * [login.py](./Sentiment_Stock_Forecaster/streamlit/components/login.py)
    * [portfolio_uploader.py](./Sentiment_Stock_Forecaster/streamlit/components/portfolio_uploader.py)
    * [register.py](./Sentiment_Stock_Forecaster/streamlit/components/register.py)
    * [upgrade_plan.py](./Sentiment_Stock_Forecaster/streamlit/components/upgrade_plan.py)
  * [scrap/](./Sentiment_Stock_Forecaster/streamlit/scrap)
    * [abc.py](./Sentiment_Stock_Forecaster/streamlit/scrap/abc.py)
    * [newspage.py](./Sentiment_Stock_Forecaster/streamlit/scrap/newspage.py)
    * [scraper.py](./Sentiment_Stock_Forecaster/streamlit/scrap/scraper.py)
    * [userinfo.db](./Sentiment_Stock_Forecaster/streamlit/scrap/userinfo.db)
  * [Dockerfile](./Sentiment_Stock_Forecaster/streamlit/Dockerfile)
  * [Home.py](./Sentiment_Stock_Forecaster/streamlit/Home.py)
  * [Login.py](./Sentiment_Stock_Forecaster/streamlit/Login.py)
  * [Welcome.py](./Sentiment_Stock_Forecaster/streamlit/Welcome.py)
  * [analysis_pipeline.py](./Sentiment_Stock_Forecaster/streamlit/analysis_pipeline.py)
  * [docker-compose.yml](./Sentiment_Stock_Forecaster/streamlit/docker-compose.yml)
  * [example_format.json](./Sentiment_Stock_Forecaster/streamlit/example_format.json)
  * [requirements.txt](./Sentiment_Stock_Forecaster/streamlit/requirements.txt)
  * [unittest_loginPage.py](./Sentiment_Stock_Forecaster/streamlit/unittest_loginPage.py)
  * [userlogs.txt](./Sentiment_Stock_Forecaster/streamlit/userlogs.txt)
* [.gitignore](./Sentiment_Stock_Forecaster/.gitignore)
* [README.md](./Sentiment_Stock_Forecaster/README.md)



