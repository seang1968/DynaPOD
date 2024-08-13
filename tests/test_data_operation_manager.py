# test_data_operation_manager.py
import unittest
from unittest.mock import patch, MagicMock
from managers.data_operation_manager import DataOperationManager
from data_source.binance_data_source import BinanceDataSource
from processing.data_ingestion_manager import DataIngestionManager

class TestDataOperationManager(unittest.TestCase):

    @patch('managers.data_operation_manager.BinanceDataSource')
    @patch('managers.data_operation_manager.DataIngestionManager')
    @patch('managers.data_operation_manager.Configuration')
    def test_perform_initial_load(self, mock_configuration, mock_data_ingestion_manager, mock_binance_data_source):
        # Arrange
        mock_config = mock_configuration.return_value
        mock_data_source = mock_binance_data_source.return_value
        mock_ingestion_manager = mock_data_ingestion_manager.return_value

        mock_ingestion_manager.run = MagicMock()

        manager = DataOperationManager(mock_config)

        # Act
        manager.perform_initial_load(pair_name='BTCUSDT', limit=1000, db_file='test.db')

        # Assert
        mock_binance_data_source.assert_called_once_with(mock_config, 'BTCUSDT')
        mock_data_ingestion_manager.assert_called_once_with(mock_config, mock_data_source, 'BTCUSDT')
        mock_ingestion_manager.run.assert_called_once_with(1000)

if __name__ == '__main__':
    unittest.main()
