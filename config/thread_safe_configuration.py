import threading
from config.configuration import Configuration

class ThreadSafeConfiguration:
    def __init__(self, config: Configuration):
        # Store the provided configuration instance
        self._config = config
        # Create a lock object for thread-safe operations
        self._lock = threading.Lock()

    def __getattr__(self, name):
        # Retrieve the attribute from the configuration instance
        attr = getattr(self._config, name)
        
        # If the attribute is a callable method, wrap it in a thread-safe function
        if callable(attr):
            def thread_safe_method(*args, **kwargs):
                with self._lock:
                    return attr(*args, **kwargs)
            return thread_safe_method
        else:
            # If not callable, return the attribute directly
            return attr
