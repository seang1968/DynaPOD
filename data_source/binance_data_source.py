import requests
import pytz
from datetime import datetime

class BinanceDataSource:
    def __init__(self, config, pair_name):
        self.config = config
        self.coin_pair = pair_name
        self.time_frame = config.get(pair_name, 'time_frame')
        self.limit = config.get(pair_name, 'limit')
        self.timezone = pytz.timezone(config.get(pair_name, 'timezone'))

    def fetch_minute_data(self):
        base_url = "https://api.binance.com"
        endpoint = f"/api/v3/klines"
        params = {
            "symbol": self.coin_pair,
            "interval": self.time_frame,
            "limit": self.limit
        }
        
        response = requests.get(base_url + endpoint, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching data: {response.status_code} - {response.text}")
            return None
