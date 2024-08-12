import unittest
from config.configuration import Configuration
from config.thread_safe_configuration import ThreadSafeConfiguration

class TestConfigurationHandling(unittest.TestCase):

    def setUp(self):
        self.config_path = 'config/pairs.xml'

    def test_standard_configuration(self):
        config = Configuration(self.config_path)
        
        self.assertEqual(config.get('ETHUSDT', 'time_frame'), '1m')
        self.assertEqual(config.get('ETHUSDT', 'limit'), 10)
        self.assertEqual(config.get('ETHUSDT', 'db_file'), 'ETHUSDT.db')
        self.assertEqual(config.get('ETHUSDT', 'timezone'), 'America/Chicago')

        self.assertEqual(config.get('BTCUSDT', 'time_frame'), '1m')
        self.assertEqual(config.get('BTCUSDT', 'limit'), 10)
        self.assertEqual(config.get('BTCUSDT', 'db_file'), 'BTCUSDT.db')
        self.assertEqual(config.get('BTCUSDT', 'timezone'), 'America/New_York')

    def test_thread_safe_configuration(self):
        config = ThreadSafeConfiguration(Configuration(self.config_path))
        
        self.assertEqual(config.get('ETHUSDT', 'time_frame'), '1m')
        self.assertEqual(config.get('ETHUSDT', 'limit'), 10)
        self.assertEqual(config.get('ETHUSDT', 'db_file'), 'ETHUSDT.db')
        self.assertEqual(config.get('ETHUSDT', 'timezone'), 'America/Chicago')

        self.assertEqual(config.get('BTCUSDT', 'time_frame'), '1m')
        self.assertEqual(config.get('BTCUSDT', 'limit'), 10)
        self.assertEqual(config.get('BTCUSDT', 'db_file'), 'BTCUSDT.db')
        self.assertEqual(config.get('BTCUSDT', 'timezone'), 'America/New_York')

if __name__ == '__main__':
    unittest.main()
