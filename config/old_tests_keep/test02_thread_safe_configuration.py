import time
import os
from config.configuration import Configuration
from config.thread_safe_configuration import ThreadSafeConfiguration
import threading

# Use an absolute path for the configuration file
config_file_path = os.path.join(os.path.dirname(__file__), 'thread_config.xml')
config = Configuration(config_file_path)

# Wrap the Configuration object with ThreadSafeConfiguration
thread_safe_config = ThreadSafeConfiguration(config)

def worker_thread(thread_id):
    """Function to be executed by each thread."""
    print(f"Thread {thread_id} starting")
    thread_safe_config.set_temporary(f'setting_thread_{thread_id}', f'value_{thread_id}', 'string')
    thread_safe_config.update_setting(f'setting_thread_{thread_id}', f'value_{thread_id}_updated', 'string')
    thread_safe_config.save()
    print(f"Thread {thread_id} finished")


if __name__ == "__main__":
    threads = []
    for i in range(10):  # Create 10 threads
        t = threading.Thread(target=worker_thread, args=(i,))  # Pass only thread_id
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("All threads have finished.")