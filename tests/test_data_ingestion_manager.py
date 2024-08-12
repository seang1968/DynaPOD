import unittest
from unittest.mock import MagicMock, patch
from config.configuration import Configuration
from data_source.binance_data_source import BinanceDataSource
from database.sqlite_database import SQLiteDatabase
from processing.data_transformer import DataTransformer
from processing.data_ingestion_manager import DataIngestionManager

class TestDataIngestionManager(unittest.TestCase):

    def setUp(self):
        # Initialize mock components
        self.config = Configuration('config/pairs.xml')
        self.mock_data_source = MagicMock(spec=BinanceDataSource)
        self.mock_transformer = MagicMock(spec=DataTransformer)
        self.mock_db = MagicMock(spec=SQLiteDatabase)

        # Patch the DataTransformer and SQLiteDatabase within DataIngestionManager
        with patch('processing.data_ingestion_manager.DataTransformer', return_value=self.mock_transformer):
            with patch('processing.data_ingestion_manager.SQLiteDatabase', return_value=self.mock_db):
                # Initialize DataIngestionManager with mocks
                self.manager = DataIngestionManager(self.config, self.mock_data_source, 'ETHUSDT')

    def test_run(self):
        # Setup mock return values
        mock_raw_data = [
            [1625097600000, "35000.00", "36000.00", "34000.00", "35500.00", "100.0", 1625097660000]
        ]
        mock_transformed_data = [{
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

        self.mock_data_source.fetch_minute_data.return_value = mock_raw_data
        self.mock_transformer.transform.return_value = mock_transformed_data

        # Run the data ingestion process
        self.manager.run()

        # Verify that the data source, transformer, and db methods were called
        self.mock_data_source.fetch_minute_data.assert_called_once()
        self.mock_transformer.transform.assert_called_once_with(mock_raw_data)
        self.mock_db.store_price_data.assert_called_once_with(mock_transformed_data, 'ETHUSDT')
        self.mock_db.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()
