# Stock Analysis Summarizer

## Application Link: http://54.147.73.127:8501

[![FastAPI Unit Tests](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/actions/workflows/pytest.yml/badge.svg)](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/actions/workflows/pytest.yml)

# Code Coverage - CodeCov
Integrated our repository with the CodeCov to get the code coverage with the tests written. <br>
Below is the codecoverage showing different files of the fastapi module of Stock Analysis Summarizer.<br>
<img src="https://codecov.io/gh/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/branch/main/graphs/sunburst.svg?token=NGU9K01WWF" alt="Code Coverage" width="200" height="200">

[![Code Coverage](https://codecov.io/gh/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/branch/main/graph/badge.svg?token=NGU9K01WWF)](https://codecov.io/gh/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer)


# CLaaT Document
https://codelabs-preview.appspot.com/?file_id=1xpThxuUEYJ5D3UqJBafAID6McqWWZlaih32qt9NzPEA#14

# Google Document
https://docs.google.com/document/d/1xpThxuUEYJ5D3UqJBafAID6McqWWZlaih32qt9NzPEA/edit?usp=sharing


# Overview

This project aims to provide summary of the analysis articles for a given portfolio of stock tickers. The data is collected from SeekingAlpha, a financial news website that publishes analysis articles on various stocks.

# Goals 🎯

 - Provide investors with quick and accurate analysis summaries: One of the main goals of your project could be to provide investors with quick and accurate summaries of analysis articles related to their portfolio of stock tickers. This could be useful for busy investors who don't have time to read through all the articles themselves, or for those who want to get a quick overview of the sentiment and news related to their portfolio.
 - Automate stock analysis research: Another goal could be to automate the process of collecting, analyzing, and summarizing stock analysis articles. This could save investors time and effort, as they would not have to manually search for and read through articles. The automated process could be set up to run periodically, providing investors with up-to-date information on their portfolio.
 - Provide insights and trends for stocks: Your project could also be used to provide insights and trends for various stocks over time. By analyzing sentiment and summarizing news articles over a period of time, you could provide investors with insights into how a particular stock is performing and any notable trends that may be emerging. This could be useful for investors who want to make informed decisions about buying, selling, or holding a particular stock.


# Use cases 

 - 💡 Investment research: Your project could be useful for investment research, as it provides an easy and automated way to collect and analyze news articles related to a portfolio of stocks. Investors can use the summarized news and sentiment analysis to make informed decisions about their investments.
 - 💡 Financial news aggregation: Your project could be useful for aggregating financial news, as it collects and summarizes news articles from SeekingAlpha, a popular financial news website. This can save time for investors who want to stay up-to-date on financial news but don't have the time to manually read through articles.
 - 💡 Automated stock analysis: Your project could automate the process of collecting and summarizing news articles related to a portfolio of stocks. This can save investors time and effort, as they don't have to manually search for and read through articles. The automated process could be set up to run periodically, providing investors with up-to-date information on their portfolio.

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
![Architecture_diagram](https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer/blob/main/stock_analysis_summarizer_arch.png)

# Workflow
- User enters a portfolio of stock tickers in the Streamlit web interface.
- The Airflow DAG is triggered to collect articles related to the provided stock tickers from SeekingAlpha.
- The collected articles are preprocessed using NLP techniques, and sentiment analysis is performed on each article.
- The results are stored in the database.
- Two summaries are generated from the sentiment analysis results: one for all positive articles and another for all negative articles.
- The summaries are displayed in the Streamlit web interface.
- TODO: add more

# Directory Structure
```
Sentiment_Stock_Forecaster/
┣ .github/
┃ ┗ workflows/
┃   ┗ pytest.yml
┣ Snowflake_SQL/
┃ ┗ create_statements.sql
┣ airflow/
┃ ┣ dags/
┃ ┃ ┣ daily_article_fetcher.py
┃ ┃ ┣ delete_old_files_dag.py
┃ ┃ ┗ new_stock_article_fetcher.py
┃ ┗ docker-compose.yaml
┣ fastapi/
┃ ┣ Authentication/
┃ ┃ ┣ __init__.py
┃ ┃ ┣ auth.py
┃ ┃ ┗ auth_bearer.py
┃ ┣ Util/
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
┃ ┣ Util/
┃ ┃ ┣ __init__.py
┃ ┃ ┣ db_conn.py
┃ ┃ ┗ db_util.py
┃ ┣ components/
┃ ┃ ┣ admin_dashboard.py
┃ ┃ ┣ analysis_vs_reality.py
┃ ┃ ┣ login.py
┃ ┃ ┣ portfolio_uploader.py
┃ ┃ ┣ register.py
┃ ┃ ┗ upgrade_plan.py
┃ ┣ Dockerfile
┃ ┣ Home.py
┃ ┣ analysis_pipeline.py
┃ ┣ example_format.json
┃ ┗ requirements.txt
┣ .env
┣ .gitignore
┣ README.md
┣ architecture.py
┣ docker-compose.yml
┗ stock_analysis_summarizer.png
```


# Local Installation 
## Streamlit & FastAPI

Step 1 -  Clone the repository on your local system using the below command and Change the directory to streamlit:
```bash
git clone https://github.com/BigDataIA-Spring2023-Team-03/Stock_Analysis_Summarizer
cd streamlit
```

Step 2 - Create Virtual Environment
```bash
python -m venv venv_streamlit
```

Step 3 - Install all the requirements by navigating to the streamlit folder and enter the command:
```bash
pip install -r requirements.txt
```

Step 4 - Run the streamlit application using the below command
```bash
streamlit run Home.py
```

Step 5 - The Application will be up on ```http://localhost:8501```

## FastAPI

Step 1 - Similarly, change the directory to fastapi and install the requirements
```bash
cd ../fastapi
```

Step 2 - Create Virtual Environment
```bash
python -m venv venv_fastapi
```

Step 3 - Install all the requirements by navigating to the streamlit folder and enter the command:
```bash
pip install -r requirements.txt
```

Step 4 - Navigate to fastapi folder and the Run the FastAPI using the following command:
```bash
uvicorn apis:app --reload
```

Step 5 - The Application will be up on ```http://localhost:8000/docs```

## (OR) FastAPI & Streamlit using docker-compose

Step 1 - Install docker and docker-compose in the local machine

Step 2 - Build and Run the docker-compose.yml file
```bash
docker-compose build
docker-compose up
```
Step 3 - The Applications will be up on ```http://localhost:8501``` and ```http://localhost:8000/docs```

## Airflow 

Step 1 - Install airflow in the local machine

Step 2 - Change the directory to airflow
```bash
cd airflow
```

Step 3 - Run the docker-compose.yml file
```bash
docker-compose up
```

Step 4 - The Application will be up on ```http://localhost:8080```

# Project Components

## Streamlit:
Streamlit is an open-source Python library used for building interactive web applications. In this project, Streamlit is used to create a user interface that allows the user to enter their portfolio of stock tickers to get their corresponding positive/negative summaries. The Streamlit web interface displays the output of the summarised and sentiment analysis performed on the collected articles from SeekingAlpha. Streamlit also handles the user login and sign-up functionalities to grant access to the Application.

## FastAPI:
FastAPI is a modern, fast (high-performance), web framework for building APIs with python. In this project, FastAPI is used to decouple the frontend and backend. It is primarily used for user related actions such as login, register, upgrading the service plan. 

## Airflow:
Airflow is an open-source platform to programmatically author, schedule, and monitor workflows. In this project, primarily 3 Airflow DAGs have been used: 
1. daily_article_fetcher.py, which keeps the articles up to date for the top 10 standard stock tickers we have picked.
2. new_article_fetcher.py, which will get triggered when user enters a new stock ticker to fetch articles for 30 days and gets the sentiments for each of the articles to categorise each into either positive or negative.
3. delete_old_files_dag.py: this dag deletes all the files older to 30 days from the S3 buckets.

## APIs:
Yahoo Finance python is used to fetch latest prices of stock tickers. Additionally, Seeking Alpha API is also used to fetch news and summary for a particular stock ticker.

## Great Expectations using docker-compose

Step 1 - Change the directory to great_expectation and install the requirements
```bash
cd ../great_expectation
```
```bash
pip install -r requirements.txt
```

Step 2 - Run the docker-compose.yml file
```bash
docker-compose up
```

Step 3 - The Airflow Applications will be up on ```http://localhost:8080```
Login to Airflow and trigger the DAG - stock_analyzer for Data Validation


Step 4 - The GE Applications will be up on ```http://localhost:5500```
Navigate to great_expectation/airflow/working_dir/great_expectations/uncommitted/data_docs/local_site/ to check the validation report

# Brief Overview and Demo
https://www.youtube.com/embed/fgqYGhZE1Us
