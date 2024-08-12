import unittest

# Discover and run all tests in the 'tests' directory
#loader = unittest.TestLoader()
#suite = loader.discover('tests')

#runner = unittest.TextTestRunner(verbosity=2)
#runner.run(suite)


# Import all the test classes from each test file
from tests.test_binance_data_source import TestBinanceDataSource
from tests.test_configuration import TestConfiguration
from tests.test_data_ingestion_manager import TestDataIngestionManager
from tests.test_data_transformer import TestDataTransformer
from tests.test_sqlite_database import TestSQLiteDatabase
from tests.test_thread_safe_configuration import TestThreadSafeConfiguration
from tests.testing_thread_config_saftey import TestThreadSafeConfiguration2
from tests.pairs_test_configuration_handling import TestConfigurationHandling
from tests.test_pairs_main import TestPairsMain
# Create a test suite
suite = unittest.TestSuite()

# Add all test cases to the suite
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestBinanceDataSource))
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestConfiguration))
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestDataIngestionManager))
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestDataTransformer))
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestSQLiteDatabase))
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestThreadSafeConfiguration))
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestThreadSafeConfiguration2))
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestConfigurationHandling))
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestPairsMain))
# Run the suite
runner = unittest.TextTestRunner(verbosity=2)
runner.run(suite)
