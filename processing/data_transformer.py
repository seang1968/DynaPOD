from datetime import datetime, timezone
import pytz
from config.configuration import Configuration

class DataTransformer:
    def __init__(self, config: Configuration, pair_name: str):
        # Use the pair name to get the correct timezone
        self.timezone = pytz.timezone(config.get(pair_name, 'timezone'))

    def transform(self, data):
        transformed_data = []
        for entry in data:
            open_epoch = entry[0]
            close_epoch = entry[6]
            open_time = datetime.fromtimestamp(open_epoch / 1000, tz=timezone.utc).astimezone(self.timezone)
            close_time = datetime.fromtimestamp(close_epoch / 1000, tz=timezone.utc).astimezone(self.timezone)
            open_price = float(entry[1])
            close_price = float(entry[4])
            
            # Calculate price change percent
            price_change_percent = ((close_price - open_price) / open_price) * 100
            price_change_percent = round(price_change_percent, 4)

            # Determine direction
            direction = "up" if close_price > open_price else "down"

            transformed_data.append({
                'open_time': open_time.strftime('%Y-%m-%d %H:%M:%S'),
                'close_time': close_time.strftime('%Y-%m-%d %H:%M:%S'),
                'open_epoch': open_epoch,
                'close_epoch': close_epoch,
                'open': open_price,
                'high': float(entry[2]),
                'low': float(entry[3]),
                'close': close_price,
                'volume': float(entry[5]),
                'price_change_percent': price_change_percent,
                'direction': direction
            })
        return transformed_data
