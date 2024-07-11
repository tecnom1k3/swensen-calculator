import requests
from decimal import Decimal
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Get the Alpha Vantage API key
alpha_vantage_api_key = os.getenv('ALPHA_VANTAGE_API_KEY')


def get_market_price(ticker):
    print(f"Retrieving market price for {ticker}...")
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={alpha_vantage_api_key}"
    response = requests.get(url)
    data = response.json()
    if "Time Series (Daily)" in data:
        last_refreshed = list(data["Time Series (Daily)"].keys())[0]
        current_price = Decimal(data["Time Series (Daily)"][last_refreshed]["4. close"])
        print(f"Market price for {ticker}: ${current_price:.2f}")
        return current_price
    else:
        print(f"Error retrieving data for {ticker}")
        return None
