import unittest
from unittest.mock import patch, MagicMock
from pairs_main import main

class TestPairsMain(unittest.TestCase):

    @patch('pairs_main.DataIngestionManager')
    @patch('pairs_main.BinanceDataSource')
    @patch('pairs_main.Configuration')
    def test_main(self, MockConfiguration, MockBinanceDataSource, MockDataIngestionManager):
        # Arrange
        mock_config = MockConfiguration.return_value
        mock_data_source = MockBinanceDataSource.return_value
        mock_ingestion_manager = MockDataIngestionManager.return_value

        # Act
        main('ETHUSDT')

        # Assert
        MockConfiguration.assert_called_once_with('config/pairs.xml')
        MockBinanceDataSource.assert_called_once_with(mock_config, 'ETHUSDT')
        MockDataIngestionManager.assert_called_once_with(mock_config, mock_data_source, 'ETHUSDT')
        mock_ingestion_manager.run.assert_called_once()

if __name__ == '__main__':
    unittest.main()
