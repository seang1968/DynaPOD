import unittest
import os
from database.sqlite_database import SQLiteDatabase

class TestSQLiteDatabase(unittest.TestCase):

    def setUp(self):
        # Use an in-memory SQLite database for testing
        self.db = SQLiteDatabase(':memory:')

    def test_table_creation(self):
        # Check that the table was created
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='price_data';")
        self.assertEqual(cursor.fetchone()[0], 'price_data')

    def test_store_price_data(self):
        # Mock data to insert into the database
        mock_data = [{
            'open_time': '2021-06-30 19:00:00',
            'close_time': '2021-06-30 19:01:00',
            'open_epoch': 1625097600000,
            'close_epoch': 1625097660000,
            'open': 35000.00,
            'high': 36000.00,
            'low': 34000.00,
            'close': 35500.00,
            'volume': 100.0,
            'price_change_percent': 1.4286,
            'direction': 'up'
        }]
        self.db.store_price_data(mock_data, 'ETHUSDT')

        # Verify that the data was inserted
        cursor = self.db.conn.cursor()
        cursor.execute("SELECT * FROM price_data WHERE coin_pair='ETHUSDT';")
        result = cursor.fetchone()

        self.assertIsNotNone(result)
        self.assertEqual(result[1], 'ETHUSDT')
        self.assertEqual(result[5], 1625097660000)
        self.assertEqual(result[9], 35500.00)
        self.assertEqual(result[12], 'up')


    def tearDown(self):
        # Close the database connection
        self.db.close()

if __name__ == '__main__':
    unittest.main()
