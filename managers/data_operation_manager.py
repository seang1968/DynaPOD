from processing.data_ingestion_manager import DataIngestionManager
from data_source.binance_data_source import BinanceDataSource
from config.configuration import Configuration

class DataOperationManager:
    def __init__(self, config_file: str):
        self.config = Configuration(config_file)

    def perform_initial_load(self, pair_name: str, limit: int):
        # Initialize the data source and ingestion manager
        data_source = BinanceDataSource(self.config, pair_name)
        ingestion_manager = DataIngestionManager(self.config, data_source, pair_name)

        # Run the data ingestion process
        print(f"Performing initial load for {pair_name} with limit {limit}")
        ingestion_manager.run(limit)
