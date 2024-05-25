
import requests

def get_stock_prices():
    response = requests.get('https://api.example.com/stock_prices')
    return response.json()
