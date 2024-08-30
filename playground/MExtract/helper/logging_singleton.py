import logging
import os
from logging.handlers import RotatingFileHandler
from helper.constants_singleton import Constants

class Logging:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            # Create logs directory if it does not exist
            if not os.path.exists(Constants().log_dir_name):
                os.makedirs(Constants().log_dir_name)

            log_file_path = os.path.join(Constants().log_dir_name, Constants().log_file_name)

            cls._instance.logger = logging.getLogger(Constants().logger_name)
            cls._instance.logger.setLevel(Constants().log_gen_level)

            # Create formatter objects
            file_formatter = logging.Formatter(Constants().logfile_file_format)
            console_formatter = logging.Formatter(Constants().logstream_format)

            # Create and configure file handler with rotation
            file_handler = RotatingFileHandler(
                log_file_path,
                maxBytes=Constants().log_file_max_bytes,  # Set max bytes for rotation
                backupCount=Constants().log_file_backup_count  # Set number of backup files to keep
            )
            file_handler.setFormatter(file_formatter)
            file_handler.setLevel(Constants().log_file_level)

            # Create and configure console handler
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(console_formatter)
            console_handler.setLevel(Constants().log_stream_level)

            # Add handlers to logger
            cls._instance.logger.addHandler(file_handler)
            cls._instance.logger.addHandler(console_handler)

            # Force rotation for testing purposes
            cls._instance.logger.handlers[0].doRollover()

        return cls._instance

    def log_df_fld_info(self, df, df_name, col_name):
        self.info(f"Analyzing {df_name} on column {col_name}")
        for value, count in (df[col_name].value_counts(dropna=False).items()):
            self.info(f"Value {value} Its count is :: {count}")

    def log(self, level, message):
        self.logger.log(level, message)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def critical(self, message):
        self.logger.critical(message)

    def error(self, message):
        self.logger.error(message)

    @staticmethod
    def close_log():
        # Flush and close handlers at the end of the program
        for handler in Logging._instance.logger.handlers:
            handler.close()
            Logging._instance.logger.removeHandler(handler)

        Logging._instance.logger = None
