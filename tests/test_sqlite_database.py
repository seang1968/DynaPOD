import unittest
from database.sqlite_database import SQLiteDatabase
from unittest.mock import MagicMock

class TestSQLiteDatabase(unittest.TestCase):
    def setUp(self):
        self.db = SQLiteDatabase(':memory:', 'test_security')
        self.db.security = 'test_security'  # Set the table name to a placeholder for in-memory

    def test_table_creation(self):
        cursor = self.db.conn.cursor()
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{self.db.security}';")
        self.assertEqual(cursor.fetchone()[0], self.db.security)

    def test_store_price_data(self):
        mock_data = [
            {'datetime': '2024-08-11T00:00:00Z', 'open': 1.0, 'high': 2.0, 'low': 0.5, 'close': 1.5, 'volume': 100},
            {'datetime': '2024-08-11T00:01:00Z', 'open': 1.5, 'high': 2.5, 'low': 1.0, 'close': 2.0, 'volume': 150}
        ]
        self.db.store_data(mock_data)
        cursor = self.db.conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {self.db.security}")
        self.assertEqual(cursor.fetchone()[0], 2)

if __name__ == '__main__':
    unittest.main()
