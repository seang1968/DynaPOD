import unittest
from unittest.mock import MagicMock, patch
from processing.data_ingestion_manager import DataIngestionManager
from database.sqlite_database import SQLiteDatabase

class TestDataIngestionManager(unittest.TestCase):

    def setUp(self):
        self.config = MagicMock()
        self.mock_data_source = MagicMock()
        self.security = 'ETHUSDT'

        # Ensure the mock returns a valid timezone
        self.config.get.return_value = 'America/New_York'

        # Mock the DataTransformer class
        with patch('processing.data_ingestion_manager.DataTransformer') as MockTransformer:
            self.mock_transformer = MockTransformer.return_value
            self.manager = DataIngestionManager(self.config, self.mock_data_source, self.security)
            self.manager.db = MagicMock(spec=SQLiteDatabase)  # Mock the SQLiteDatabase class

    def test_run(self):
        # Setup mock data and methods
        mock_raw_data = [
            [
                1609459200000,  # Open time (timestamp)
                '1.0',          # Open price
                '2.0',          # High price
                '0.5',          # Low price
                '1.5',          # Close price
                '1000',         # Volume
                1609459260000   # Close time (timestamp)
            ],
        ]
        self.mock_data_source.fetch_minute_data.return_value = mock_raw_data

        # Run the manager
        self.manager.run()

        # Ensure the transform method was called with the right data
        self.mock_transformer.transform.assert_called_once_with(mock_raw_data)

if __name__ == '__main__':
    unittest.main()
