import sqlite3
import os

class SQLiteDatabase:
    def __init__(self, db_file, security):
        # Ensure the old database is removed before starting the test
        if os.path.exists(db_file):
            os.remove(db_file)
        
        self.db_file = db_file
        self.security = security
        self.conn = sqlite3.connect(self.db_file)
        self._create_table()

    def _create_table(self):
        cursor = self.conn.cursor()
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {self.security} (
                datetime TEXT PRIMARY KEY,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                volume REAL
            )
        ''')
        self.conn.commit()

    def store_data(self, data):
        cursor = self.conn.cursor()
        for entry in data:
            cursor.execute(f'''
                INSERT INTO {self.security} (datetime, open, high, low, close, volume)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (entry['datetime'], entry['open'], entry['high'], entry['low'], entry['close'], entry['volume']))
        self.conn.commit()

    def get_latest_timestamp(self):
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT MAX(datetime) FROM {self.security}")
        result = cursor.fetchone()[0]
        return result
