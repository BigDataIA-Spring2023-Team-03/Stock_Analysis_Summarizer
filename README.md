# Stock Analysis Summarizer

## Application Link: http://54.147.73.127:8501

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

# Detailed User Process

When a user logs in or signs up on the Streamlit application, they are granted access to the features of the application. One of these features is the GPT API, which allows the user to get the ticker name for a particular company. To use this feature, the user enters the ticker/tickers in the Streamlit web interface. When the user enters the ticker, an Airflow DAG is triggered to collect articles related to the provided stock tickers from SeekingAlpha. Once the articles are collected, they are preprocessed using Natural Language Processing (NLP) techniques, and sentiment analysis is performed on each article using the Procus-Finbert model. This model determines whether the article is positive or negative towards the company. All positive articles are then summarized into one positive summary, and the same is done for negative articles. The results are then stored in an S3 bucket. Finally, the summaries are displayed in the Streamlit web interface for the user to view. This entire process involves a series of technical steps that utilize different technologies to ensure accurate results and a seamless user experience.

# Technologies Used
![Python](https://img.shields.io/badge/python-grey?style=for-the-badge&logo=python&logoColor=ffdd54)
![](https://img.shields.io/badge/FastAPI-4285F4?style=for-the-badge&logo=fastapi&logoColor=white)
![](https://img.shields.io/badge/SeekingAlpha-orange?style=for-the-badge&logo=seeking-alpha&logoColor=white)
![](https://img.shields.io/badge/GitHub_Actions-green?style=for-the-badge&logo=github-actions&logoColor=white)
![](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![](https://img.shields.io/badge/Snowflake-blue?style=for-the-badge&logo=Snowflake&logoColor=white)

# Architecture
![Architecture_diagram](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/blob/main/stock_analysis_summarizer.png)

# Workflow
- User enters a portfolio of stock tickers in the Streamlit web interface.
- The Airflow DAG is triggered to collect articles related to the provided stock tickers from SeekingAlpha.
- The collected articles are preprocessed using NLP techniques, and sentiment analysis is performed on each article.
- The results are stored in the database.
- Two summaries are generated from the sentiment analysis results: one for all positive articles and another for all negative articles.
- The summaries are displayed in the Streamlit web interface.
- TODO: add more

# Directory Structure

* [.github/](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/.github)
  * [workflows/](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/.github/workflows)
    * [pytest.yml](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/.github/workflows/pytest.yml)
* [Snowflake_SQL/](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/Snowflake_SQL)
  * [create_statements.sql](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/Snowflake_SQL/create_statements.sql)
* [airflow/](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/airflow)
  * [dags/](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/airflow/dags)
    * [daily_article_fetcher.py](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/airflow/dags/daily_article_fetcher.py)
    * [daily_article_fetcher_copy.py](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/airflow/dags/daily_article_fetcher_copy.py)
    * [new_stock_article_fetcher.py](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/airflow/dags/new_stock_article_fetcher.py)
  * [docker-compose.yaml](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/airflow/docker-compose.yaml)
* [fastapi/](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/fastapi)
  * [Authentication/](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/fastapi/Authentication)
    * [__pycache__/](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/fastapi/Authentication/__pycache__)
      * [__init__.cpython-311.pyc](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/fastapi/Authentication/__pycache__/__init__.cpython-311.pyc)
      * [auth.cpython-311.pyc](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/fastapi/Authentication/__pycache__/auth.cpython-311.pyc)
      * [auth_bearer.cpython-311.pyc](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/fastapi/Authentication/__pycache__/auth_bearer.cpython-311.pyc)
    * [__init__.py](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/fastapi/Authentication/__init__.py)
    * [auth.py](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/fastapi/Authentication/auth.py)
    * [auth_bearer.py](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/fastapi/Authentication/auth_bearer.py)
  * [Util/](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/fastapi/Util)
    * [__pycache__/](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/fastapi/Util/__pycache__)
      * [__init__.cpython-311.pyc](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/fastapi/Util/__pycache__/__init__.cpython-311.pyc)
      * [db_conn.cpython-311.pyc](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/fastapi/Util/__pycache__/db_conn.cpython-311.pyc)
      * [db_util.cpython-311.pyc](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/fastapi/Util/__pycache__/db_util.cpython-311.pyc)
    * [__init__.py](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/fastapi/Util/__init__.py)
    * [db_conn.py](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/fastapi/Util/db_conn.py)
    * [db_util.py](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/fastapi/Util/db_util.py)
  * [__pycache__/](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/fastapi/__pycache__)
    * [apis.cpython-311.pyc](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/fastapi/__pycache__/apis.cpython-311.pyc)
    * [schemas.cpython-311.pyc](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/fastapi/__pycache__/schemas.cpython-311.pyc)
  * [Dockerfile](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/fastapi/Dockerfile)
  * [apis.py](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/fastapi/apis.py)
  * [requirements.txt](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/fastapi/requirements.txt)
  * [schemas.py](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/fastapi/schemas.py)
  * [test_apis.py](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/fastapi/test_apis.py)
* [streamlit/](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/streamlit)
  * [.test/](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/streamlit/.test)
    * [include/](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/streamlit/.test/include)
      * [python3.11/](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/streamlit/.test/include/python3.11)
    * [lib/](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/streamlit/.test/lib)
      * [python3.11/](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/streamlit/.test/lib/python3.11)
        * [site-packages/](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/streamlit/.test/lib/python3.11/site-packages)
  * [Util/](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/streamlit/Util)
    * [__pycache__/](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/streamlit/Util/__pycache__)
      * [__init__.cpython-311.pyc](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/streamlit/Util/__pycache__/__init__.cpython-311.pyc)
      * [db_conn.cpython-311.pyc](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/streamlit/Util/__pycache__/db_conn.cpython-311.pyc)
      * [db_util.cpython-311.pyc](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/streamlit/Util/__pycache__/db_util.cpython-311.pyc)
    * [.env](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/streamlit/Util/.env)
    * [__init__.py](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/streamlit/Util/__init__.py)
    * [db_conn.py](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/streamlit/Util/db_conn.py)
    * [db_util.py](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/streamlit/Util/db_util.py)
  * [components/](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/streamlit/components)
    * [__pycache__/](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/streamlit/components/__pycache__)
      * [admin_dashboard.cpython-311.pyc](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/streamlit/components/__pycache__/admin_dashboard.cpython-311.pyc)
      * [analysis_vs_reality.cpython-311.pyc](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/streamlit/components/__pycache__/analysis_vs_reality.cpython-311.pyc)
      * [login.cpython-311.pyc](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/streamlit/components/__pycache__/login.cpython-311.pyc)
      * [portfolio_uploader.cpython-311.pyc](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/streamlit/components/__pycache__/portfolio_uploader.cpython-311.pyc)
      * [register.cpython-311.pyc](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/streamlit/components/__pycache__/register.cpython-311.pyc)
      * [upgrade_plan.cpython-311.pyc](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/streamlit/components/__pycache__/upgrade_plan.cpython-311.pyc)
    * [admin_dashboard.py](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/streamlit/components/admin_dashboard.py)
    * [analysis_vs_reality.py](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/streamlit/components/analysis_vs_reality.py)
    * [login.py](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/streamlit/components/login.py)
    * [portfolio_uploader.py](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/streamlit/components/portfolio_uploader.py)
    * [register.py](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/streamlit/components/register.py)
    * [upgrade_plan.py](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/streamlit/components/upgrade_plan.py)
  * [scrap/](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/streamlit/scrap)
    * [abc.py](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/streamlit/scrap/abc.py)
    * [newspage.py](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/streamlit/scrap/newspage.py)
    * [scraper.py](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/streamlit/scrap/scraper.py)
    * [userinfo.db](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/streamlit/scrap/userinfo.db)
  * [Dockerfile](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/streamlit/Dockerfile)
  * [Home.py](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/streamlit/Home.py)
  * [Welcome.py](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/streamlit/Welcome.py)
  * [analysis_pipeline.py](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/streamlit/analysis_pipeline.py)
  * [example_format.json](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/streamlit/example_format.json)
  * [requirements.txt](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/streamlit/requirements.txt)
* [.env](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/.env)
* [.gitignore](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/.gitignore)
* [README.md](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/README.md)
* [arch.py](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/arch.py)
* [docker-compose.yml](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/docker-compose.yml)
* [stock_analysis_summarizer](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/stock_analysis_summarizer)

# Local Installation
Local Installation

Step 1 -  Clone the repository on your local system using the below command :
```bash
git clone https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer
```

Step 2 - Install all the requirements by navigating to the streamlit folder and enter the command:
```bash
pip install -r requirements.txt
```
Step 3 - open terminal in local system or in VSCode and navigate into the Stock_Analysis_Summarizer

Step 4 - Navigate to fastapi folder and the Run the FastAPI using the following command:
```bash
uvicorn api.py:app --reload --port:8000
```

Step 5 - Open a new terminal without stopping FASTAPI and navigate to streamlit folder and run streamlit app: 
```bash
streamlit run Home.py
```
