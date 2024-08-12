import unittest
import os
from config.configuration import Configuration

class TestConfiguration(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Create a fresh test XML file."""
        cls.test_config_file = 'test_config.xml'
        with open(cls.test_config_file, 'w') as f:
            f.write('''<config>
    <setting name="coin_pair" type="string" value="BTCUSDT" />
    <setting name="time_frame" type="string" value="1m" />
    <setting name="limit" type="integer" value="100" />
    <setting name="timezone" type="string" value="America/New_York" />
</config>''')

    @classmethod
    def tearDownClass(cls):
        """Clean up the test XML file."""
        if os.path.exists(cls.test_config_file):
            os.remove(cls.test_config_file)

    def setUp(self):
        """Instantiate the Configuration class with the test file before each test."""
        self.config = Configuration(self.test_config_file)

    def test_loading(self):
        """Test loading of configurations."""
        self.assertEqual(self.config.get('coin_pair'), "BTCUSDT")
        self.assertEqual(self.config.get('time_frame'), "1m")
        self.assertEqual(self.config.get('limit'), 100)
        self.assertEqual(self.config.get('timezone'), "America/New_York")

    def test_get_with_default(self):
        """Test retrieval of settings with default."""
        self.assertEqual(self.config.get_with_default('non_existing_setting', "default_value", 'string'), "default_value")
        self.assertEqual(self.config.get('non_existing_setting'), "default_value")

    def test_update_setting(self):
        """Test updating an existing setting."""
        self.config.update_setting('coin_pair', 'ETHUSDT', 'string')
        self.assertEqual(self.config.get('coin_pair'), "ETHUSDT")

    def test_update_or_create_setting(self):
        """Test adding a new setting."""
        self.config.update_or_create_setting('new_setting', 'new_value', 'string')
        self.assertEqual(self.config.get('new_setting'), "new_value")

    def test_delete_setting(self):
        """Test deleting a setting."""
        self.config.update_or_create_setting('new_setting', 'new_value', 'string')
        self.config.delete_setting('new_setting')
        with self.assertRaises(KeyError):
            self.config.get('new_setting')


if __name__ == "__main__":
    unittest.main()
