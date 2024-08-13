import sqlite3
import os

class SQLiteDatabase:
    def __init__(self, db_file):
        # Ensure the database file is created in the provided path
        self.db_file = db_file
        self.connection = sqlite3.connect(self.db_file)
        self._create_table()

    def _create_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS price_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                open_time TEXT,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                volume REAL
            )
        ''')
        self.connection.commit()

    def store_data(self, data):
        cursor = self.connection.cursor()
        for entry in data:
            cursor.execute('''
                INSERT INTO price_data (open_time, open, high, low, close, volume)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (entry['open_time'], entry['open'], entry['high'], entry['low'], entry['close'], entry['volume']))
        self.connection.commit()

    def close(self):
        self.connection.close()
