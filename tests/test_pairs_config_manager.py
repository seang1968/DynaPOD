# test_pairs_config_manager.py
import unittest
from managers.pairs_config_manager import PairsConfigManager

class TestPairsConfigManager(unittest.TestCase):

    def setUp(self):
        self.pairs_manager = PairsConfigManager('config/pairs.xml')

    def test_check_and_add_pair(self):
        # Clear out existing configuration for this test, if necessary
        self.pairs_manager.config.delete_pair('1INCHUSDT')
        result = self.pairs_manager.check_and_add_pair('1INCHUSDT')
        self.assertTrue(result)  # Should return True after adding the pair

    def test_pair_does_not_exist(self):
        result = self.pairs_manager.check_and_add_pair('NONEXISTENTPAIR')
        self.assertFalse(result)  # This pair should not exist on Binance

if __name__ == '__main__':
    unittest.main()

