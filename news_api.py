import requests

API_KEY = "0779f4e35c154857bf872255c48aa5d2"

def check_news(query):
    try:
        url = f"https://newsapi.org/v2/everything?q={query}&apiKey={API_KEY}"
        response = requests.get(url).json()

        articles = response.get("articles", [])

        if len(articles) > 3:
            return "Verified by multiple sources"
        else:
            return "No strong verification found"

    except:
        return "API Error / No Internet"