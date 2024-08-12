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

    def fetch_minute_data(self, limit=None):
        # If a limit is provided, use it; otherwise, use the default limit from config
        if limit is None:
            limit = self.limit
        
        base_url = "https://api.binance.com"
        endpoint = f"/api/v3/klines"
        params = {
            "symbol": self.coin_pair,
            "interval": self.time_frame,
            "limit": limit
        }
        
        response = requests.get(base_url + endpoint, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching data: {response.status_code} - {response.text}")
            return None
