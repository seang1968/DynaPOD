import unittest
from config.configuration import Configuration
from data_source.binance_data_source import BinanceDataSource

class TestBinanceDataSource(unittest.TestCase):

    def setUp(self):
        # Initialize the configuration with the XML file
        self.config = Configuration('config/pairs.xml')
        # Pass the pair name 'ETHUSDT' to BinanceDataSource
        self.data_source = BinanceDataSource(self.config, 'ETHUSDT')

    def test_fetch_minute_data(self):
        # Fetch the data and check the response structure
        data = self.data_source.fetch_minute_data()
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)
        self.assertIsInstance(data[0], list)
        print("Data fetched successfully")

if __name__ == '__main__':
    unittest.main()
