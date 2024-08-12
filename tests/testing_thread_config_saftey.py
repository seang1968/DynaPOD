import unittest
import threading
from config.thread_safe_configuration import ThreadSafeConfiguration

class MockConfiguration:
    """A mock configuration class used for testing the ThreadSafeConfiguration."""
    def __init__(self, value):
        self.value = value
    
    def get_value(self):
        return self.value
    
    def set_value(self, new_value):
        self.value = new_value

class TestThreadSafeConfiguration2(unittest.TestCase):
    
    def setUp(self):
        """Set up the mock configuration and thread-safe wrapper before each test."""
        self.config = MockConfiguration(10)
        self.thread_safe_config = ThreadSafeConfiguration(self.config)

    def test_thread_safety(self):
        """Test that the ThreadSafeConfiguration works correctly across multiple threads."""
        threads = []
        for _ in range(10):
            thread = threading.Thread(target=self.thread_safe_test_function)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        # After all threads have run, check if the value has been incremented correctly
        self.assertEqual(self.thread_safe_config.get_value(), 20)

    def thread_safe_test_function(self):
        """Function to be run by multiple threads to test thread safety."""
        current_value = self.thread_safe_config.get_value()
        self.thread_safe_config.set_value(current_value + 1)

if __name__ == "__main__":
    unittest.main()
