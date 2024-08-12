import unittest
from config.configuration import Configuration
from processing.data_transformer import DataTransformer

class TestDataTransformer(unittest.TestCase):

    def setUp(self):
        self.config = Configuration('config/pairs.xml')
        # Pass the pair name 'ETHUSDT' to DataTransformer
        self.transformer = DataTransformer(self.config, 'ETHUSDT')

    def test_empty_data(self):
        transformed_data = self.transformer.transform([])
        self.assertEqual(transformed_data, [])

    def test_transform(self):
        raw_data = [
            [1625097600000, "35000.00", "36000.00", "34000.00", "35500.00", "100.0", 1625097660000]
        ]
        transformed_data = self.transformer.transform(raw_data)
        expected_data = [{
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
        self.assertEqual(transformed_data, expected_data)

if __name__ == '__main__':
    unittest.main()
