# data_operation_manager.py
from processing.data_ingestion_manager import DataIngestionManager
from data_source.binance_data_source import BinanceDataSource
from config.configuration import Configuration
import os

class DataOperationManager:
    def __init__(self, config):
        # If config is a string, load the configuration file
        if isinstance(config, str):
            self.config = Configuration(config)
        else:
            self.config = config

    def perform_initial_load(self, pair_name: str, limit: int, db_file=None):
        # Initialize the data source and ingestion manager
        data_source = BinanceDataSource(self.config, pair_name)
        ingestion_manager = DataIngestionManager(self.config, data_source, pair_name)

        # Ensure the database is stored in the 'databases/' directory
        if not db_file:
            db_file = self.config.get(pair_name, 'db_file')
        db_path = os.path.join('databases', db_file)
        os.makedirs('databases', exist_ok=True)

        # Update the database file path in the configuration
        self.config.update_or_create_setting(pair_name, 'db_file', db_path)

        # Run the data ingestion process
        print(f"Performing initial load for {pair_name} with limit {limit}")
        ingestion_manager.run(limit)
