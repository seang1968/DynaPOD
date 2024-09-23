import logging
from logging.handlers import RotatingFileHandler
import os

class LogManager:
    def __init__(self, resource_manager):
        self.logger = None
        self.resource_manager = resource_manager  # ResourceManager is injected

    def setup_logging(self, log_file, log_level=logging.INFO, file_log_level=logging.DEBUG, max_bytes=1048576, backup_count=5):

#    def setup_logging(self,  log_level=logging.INFO, file_log_level=logging.DEBUG, max_bytes=1048576, backup_count=5):
        # Get the log folder from ResourceManager
  #      log_file = self.resource_manager.get_resource("LogFile")
        log_folder = self.resource_manager.get_resource("LogFolder")

        # Ensure the log folder exists
        if not os.path.exists(log_folder):
            os.makedirs(log_folder)
            print(f"Created log folder: {log_folder}")
        else:
            print(f"Using existing log folder: {log_folder}")

        # Construct the full log file path
        full_log_path = os.path.join(log_folder, log_file)

        # Set up the logger
        self.logger = logging.getLogger("AppLogger")
        self.logger.setLevel(logging.DEBUG)  # Set root logger to DEBUG to capture all messages

        # File handler with rotation
        file_handler = RotatingFileHandler(full_log_path, maxBytes=max_bytes, backupCount=backup_count)
        file_handler.setLevel(file_log_level)  # Lower level for file logging (DEBUG)
        file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)  # Higher level for console logging (INFO)
        console_formatter = logging.Formatter('%(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)

        # Adding handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

        # Log the log folder and log file path for confirmation
        print(f"Logging to file: {full_log_path}")

        # Force a log rotation on each run
        file_handler.doRollover()

    def get_logger(self):
        return self.logger
