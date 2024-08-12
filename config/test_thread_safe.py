import threading
from config.configuration import Configuration
from config.thread_safe_configuration import ThreadSafeConfiguration

# Mock Configuration class for testing
class MockConfiguration:
    def __init__(self, value):
        self.value = value
    
    def get_value(self):
        return self.value
    
    def set_value(self, new_value):
        self.value = new_value

# Run the tests
if __name__ == "__main__":
# Instantiate the mock configuration
    config = MockConfiguration(10)

# Create a thread-safe wrapper around it
    thread_safe_config = ThreadSafeConfiguration(config)

# Test function to run in threads
    def test_thread_safe_config():
    # Try to access and modify the value in the config
        current_value = thread_safe_config.get_value()
        print(f"Current Value: {current_value}")
        thread_safe_config.set_value(current_value + 1)

# Create multiple threads to test thread safety
    threads = []
    for _ in range(10):
        thread = threading.Thread(target=test_thread_safe_config)
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

# Final value after all threads have run
    print(f"Final Value: {thread_safe_config.get_value()}")
