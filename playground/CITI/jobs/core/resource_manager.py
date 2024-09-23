import os
import logging  # Add this import statement
from core.log_manager import LogManager

class ResourceManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ResourceManager, cls).__new__(cls)
            cls._instance.resources = {}
        return cls._instance

    def __init__(self):
        self.log_manager = LogManager(self)  # Inject ResourceManager into LogManager

    def load_resource(self, resource_config):
        resource_type = resource_config.attrib['type']
        resource_name = resource_config.attrib['name']

        if resource_type == 'sqlite':
            path = resource_config.find('path').text
            self.resources[resource_name] = self._open_sqlite(path)
        elif resource_type == 'file' and resource_name == "LogFile":
            # Setup logging (log_folder handled internally in LogManager)
            self.log_manager.setup_logging(
                log_file=resource_config.find('path').text,  # File name
                log_level=self._get_log_level(resource_config.find('console_log_level').text),
                file_log_level=self._get_log_level(resource_config.find('file_log_level').text),
                max_bytes=int(resource_config.find('max_bytes').text),
                backup_count=int(resource_config.find('backup_count').text)
            )
            self.resources[resource_name] = self.log_manager.get_logger()
        elif resource_type == 'folder':
            path = resource_config.find('path').text
            self.resources[resource_name] = self._create_or_verify_folder(path)
        else:
            raise ValueError(f"Unknown resource type: {resource_type}")

    def _get_log_level(self, level):
        """Helper method to convert log level text to logging constants."""
        return getattr(logging, level.upper(), logging.INFO)

    def _open_sqlite(self, path):
        print(f"Opening SQLite database at {path}")
        return f"SQLite connection to {path}"

    def _create_or_verify_folder(self, path):
        if not os.path.exists(path):
            os.makedirs(path)  # Create the folder if it doesn't exist
            print(f"Created folder at {path}")
        else:
            print(f"Using existing folder at {path}")
        return path

    @classmethod
    def get_resource(cls, resource_name):
        if cls._instance and resource_name in cls._instance.resources:
            return cls._instance.resources[resource_name]
        raise ValueError(f"Resource {resource_name} not found")
