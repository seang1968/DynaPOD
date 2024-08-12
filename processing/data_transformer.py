import pytz
from datetime import datetime

class DataTransformer:
    def __init__(self, config, pair_name):
        self.config = config
        self.pair_name = pair_name
        self.timezone = pytz.timezone(config.get(pair_name, 'timezone'))

    def transform(self, data):
        print("Debug: Raw data passed to transform:")
        print(data)

        transformed_data = []
        for entry in data:
            try:
                print(f"Debug: Processing entry: {entry}")
                open_epoch = entry[0]
                close_epoch = entry[6]
                open_time = datetime.fromtimestamp(open_epoch / 1000, self.timezone)
                close_time = datetime.fromtimestamp(close_epoch / 1000, self.timezone)

                transformed_entry = {
                    'open_time': open_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'close_time': close_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'open_epoch': open_epoch,
                    'close_epoch': close_epoch,
                    'open': float(entry[1]),
                    'high': float(entry[2]),
                    'low': float(entry[3]),
                    'close': float(entry[4]),
                    'volume': float(entry[5]),
                    'price_change_percent': round(((float(entry[4]) - float(entry[1])) / float(entry[1])) * 100, 4),
                    'direction': 'up' if float(entry[4]) >= float(entry[1]) else 'down'
                }
                transformed_data.append(transformed_entry)
            except IndexError as e:
                print(f"Error: {e}")
                print(f"Skipping entry due to incorrect structure: {entry}")
            except Exception as e:
                print(f"Unexpected error: {e}")
                print(f"Entry causing the issue: {entry}")
                raise

        print("Debug: Transformed data:")
        print(transformed_data)

        return transformed_data
