import sys
import argparse
from config.configuration import Configuration
from data_source.binance_data_source import BinanceDataSource
from processing.data_ingestion_manager import DataIngestionManager

def perform_initial_load(pair_name: str, config: Configuration, limit: int):
    # Load initial live data with specified limit
    print(f"Performing initial load for {pair_name} with limit {limit}")
    data_source = BinanceDataSource(config, pair_name)
    ingestion_manager = DataIngestionManager(config, data_source, pair_name)
    ingestion_manager.run(limit)

def perform_update_future(pair_name: str, config: Configuration):
    # Update with future records
    print(f"Updating future records for {pair_name}")
    data_source = BinanceDataSource(config, pair_name)
    ingestion_manager = DataIngestionManager(config, data_source, pair_name)
    ingestion_manager.run()

def manage_historical_data(pair_name: str, config: Configuration):
    # Manage historical data and fill gaps
    print(f"Managing historical data for {pair_name}")
    # Placeholder for actual implementation
    # You might want to iterate and load historical data here, managing any gaps

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Manage cryptocurrency data ingestion.")
    parser.add_argument("-pair", type=str, required=True, help="The cryptocurrency pair to process, e.g., 'ETHUSDT'.")
    parser.add_argument("-operation", type=str, required=True, choices=["initialLoad", "updateFuture", "manageHistory"], help="The operation to perform: initialLoad, updateFuture, or manageHistory.")
    parser.add_argument("-limit", type=int, help="Override the limit for data ingestion.")
    
    # Parse the arguments
    args = parser.parse_args()

    # Load configuration
    config = Configuration('config/pairs.xml')

    # Override config settings if necessary
    if args.limit:
        config.update_or_create_setting(args.pair, 'limit', str(args.limit))

    # Execute the specified operation
    if args.operation == "initialLoad":
        perform_initial_load(args.pair, config, args.limit or int(config.get(args.pair, 'limit')))
    elif args.operation == "updateFuture":
        perform_update_future(args.pair, config)
    elif args.operation == "manageHistory":
        manage_historical_data(args.pair, config)

if __name__ == '__main__':
    main()
