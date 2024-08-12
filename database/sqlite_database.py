import sqlite3
import os

class SQLiteDatabase:
    def __init__(self, security: str, db_dir: str = 'databases'):
        if security == ':memory:':
            # Use an in-memory database
            self.conn = sqlite3.connect(':memory:')
        else:
            # Create the directory for databases if it doesn't exist
            os.makedirs(db_dir, exist_ok=True)
            
            # Set the database filename based on the security symbol
            db_file = os.path.join(db_dir, f'{security}.db')
            self.conn = sqlite3.connect(db_file)
        
        self._create_table()

    def _create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS price_data (
                id INTEGER PRIMARY KEY,
                coin_pair TEXT,
                open_time TEXT,
                close_time TEXT,
                open_epoch INTEGER,
                close_epoch INTEGER,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                volume REAL,
                price_change_percent REAL,
                direction TEXT
            )
        ''')
        self.conn.commit()

    def store_price_data(self, data, coin_pair: str):
        cursor = self.conn.cursor()
        for entry in data:
            cursor.execute('''
                INSERT INTO price_data (
                    coin_pair, open_time, close_time, open_epoch, close_epoch, open, high, low, close, volume, price_change_percent, direction
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                coin_pair, entry['open_time'], entry['close_time'], entry['open_epoch'], entry['close_epoch'],
                entry['open'], entry['high'], entry['low'], entry['close'], entry['volume'],
                entry['price_change_percent'], entry['direction']
            ))
        self.conn.commit()

    def close(self):
        self.conn.close()
