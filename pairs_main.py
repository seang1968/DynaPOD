# pairs_main.py

from config.configuration import Configuration
from data_source.binance_data_source import BinanceDataSource
from processing.data_ingestion_manager import DataIngestionManager

def main(pair_name: str):
    # Load configuration
    config = Configuration('config/pairs.xml')
    
    # Create the data source and ingestion manager
    data_source = BinanceDataSource(config, pair_name)
    ingestion_manager = DataIngestionManager(config, data_source, pair_name)
    
    # Run the ingestion process
    ingestion_manager.run()

if __name__ == '__main__':
    # Pass the pair name dynamically
    main('ETHUSDT')
