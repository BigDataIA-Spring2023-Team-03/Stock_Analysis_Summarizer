import requests

def news_api_call(news_api_key):
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "q": "finance",
        "category": "business",
        "apiKey": news_api_key
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data["articles"]

def alpha_vantage_api_call(api_key):
    url = 'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers=AAPL&apikey=' + api_key
    r = requests.get(url)
    data = r.json()
    return data


