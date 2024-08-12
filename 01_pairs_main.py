import sys
import argparse
from config.configuration import Configuration
from data_source.binance_data_source import BinanceDataSource
from processing.data_ingestion_manager import DataIngestionManager

def perform_initial_load(pair_name: str, config: Configuration, limit: int):
    print(f"Performing initial load for {pair_name} with limit {limit}")
    data_source = BinanceDataSource(config, pair_name)
    ingestion_manager = DataIngestionManager(config, data_source, pair_name)
    ingestion_manager.run(limit)

def perform_update_future(pair_name: str, config: Configuration):
    print(f"Updating future records for {pair_name}")
    data_source = BinanceDataSource(config, pair_name)
    ingestion_manager = DataIngestionManager(config, data_source, pair_name)
    ingestion_manager.run()

def manage_historical_data(pair_name: str, config: Configuration):
    print(f"Managing historical data for {pair_name}")
    # Placeholder for actual implementation

def check_pair_exists(pair_name: str, config: Configuration = None):
    data_source = BinanceDataSource(pair_name=pair_name)
    if data_source.pair_exists():
        print(f"The pair {pair_name} is available on Binance.")
    else:
        print(f"The pair {pair_name} is NOT available on Binance.")

def main():
    parser = argparse.ArgumentParser(description="Manage cryptocurrency data ingestion.")
    parser.add_argument("-pair", type=str, help="The cryptocurrency pair to process, e.g., 'ETHUSDT'.")
    parser.add_argument("-operation", type=str, choices=["initialLoad", "updateFuture", "manageHistory"], help="The operation to perform: initialLoad, updateFuture, or manageHistory.")
    parser.add_argument("-limit", type=int, help="Override the limit for data ingestion.")
    parser.add_argument("-testpair", type=str, help="The cryptocurrency pair to test, e.g., '1INCHUSDT'.")

    args = parser.parse_args()

    config = Configuration('config/pairs.xml')

    if args.testpair:
        check_pair_exists(args.testpair, config)
    else:
        pair_name = args.pair
        if args.limit:
            config.update_or_create_setting(pair_name, 'limit', str(args.limit))

        if args.operation == "initialLoad":
            limit = args.limit if args.limit else int(config.get(pair_name, 'limit'))
            perform_initial_load(pair_name, config, limit)
        elif args.operation == "updateFuture":
            perform_update_future(pair_name, config)
        elif args.operation == "manageHistory":
            manage_historical_data(pair_name, config)

if __name__ == '__main__':
    main()
