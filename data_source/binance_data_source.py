import requests
import pytz
from datetime import datetime

class BinanceDataSource:
    def __init__(self, config=None, pair_name=None):
        if config and pair_name:
            self.config = config
            self.coin_pair = pair_name
            self.time_frame = config.get(pair_name, 'time_frame')
            self.limit = config.get(pair_name, 'limit')
            self.timezone = pytz.timezone(config.get(pair_name, 'timezone'))
        elif pair_name:
            self.coin_pair = pair_name

    def fetch_minute_data(self, limit=None):
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

    def fetch_minute_data_since(self, since_timestamp, limit):
        """Fetch minute data starting from the given timestamp."""
        base_url = "https://api.binance.com"
        endpoint = f"/api/v3/klines"
        params = {
            "symbol": self.coin_pair,
            "interval": self.time_frame,
            "startTime": int(since_timestamp) * 1000,
            "limit": limit
        }
        
        response = requests.get(base_url + endpoint, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching data: {response.status_code} - {response.text}")
            return None

    def pair_exists(self):
        base_url = "https://api.binance.com"
        endpoint = f"/api/v3/exchangeInfo"
        
        response = requests.get(base_url + endpoint)
        if response.status_code == 200:
            exchange_info = response.json()
            for symbol in exchange_info['symbols']:
                if symbol['symbol'] == self.coin_pair:
                    return True
            return False
        else:
            print(f"Error fetching exchange info: {response.status_code} - {response.text}")
            return False
