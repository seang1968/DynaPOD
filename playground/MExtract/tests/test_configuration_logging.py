import unittest
from helper.constants_singleton import Constants
from helper.logging_singleton import Logging

class TestConfigurationLogging(unittest.TestCase):

    def test_constants_loading(self):
        constants = Constants()
        self.assertEqual(constants.log_dir_name, "logs")
        self.assertEqual(constants.logger_name, "MyLogger")
        self.assertEqual(constants.log_gen_level, "DEBUG")

    def test_logging(self):
        logger = Logging()
        logger.info("This is an info message.")
        logger.debug("This is a debug message.")
        logger.warning("This is a warning message.")
        logger.error("This is an error message.")
        logger.critical("This is a critical message.")
        Logging.close_log()

if __name__ == "__main__":
    unittest.main()
