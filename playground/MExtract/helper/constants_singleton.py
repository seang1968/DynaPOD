from helper.configuration import Configuration

class Constants:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            # Initialize Configuration
            cls._instance.config = Configuration("config/config.xml")

            # Load constants with fallback to default values
            cls._instance.log_dir_name = cls._instance.config.get("log_dir_name") or "logs"
            cls._instance.logger_name = cls._instance.config.get("logger_name") or "MyLogger"
            cls._instance.log_gen_level = cls._instance.config.get("log_gen_level") or "DEBUG"
            cls._instance.log_file_name = cls._instance.config.get("log_file_name") or "application.log"
            cls._instance.log_file_max_bytes = cls._instance.config.get("log_file_max_bytes") or 10485760  # 10 MB
            cls._instance.log_file_backup_count = cls._instance.config.get("log_file_backup_count") or 5
            cls._instance.log_file_level = cls._instance.config.get("log_file_level") or "DEBUG"
            cls._instance.log_stream_level = cls._instance.config.get("log_stream_level") or "INFO"
            cls._instance.logfile_file_format = cls._instance.config.get("logfile_file_format") or "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            cls._instance.logstream_format = cls._instance.config.get("logstream_format") or "%(name)s - %(levelname)s - %(message)s"

        return cls._instance

    def reload_config(cls):
        """Method to reload the configuration from the XML file."""
        cls._instance.config.load()

# Example usage
constants = Constants()

# Accessing a constant
print(constants.log_dir_name)  # Should print the value from config.xml or "logs" if not present
