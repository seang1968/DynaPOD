import sys
import argparse
from managers.pairs_config_manager import PairsConfigManager
from managers.data_operation_manager import DataOperationManager
import os

def main():
    parser = argparse.ArgumentParser(description="Manage cryptocurrency data ingestion.")
    parser.add_argument("-pair", type=str, help="The cryptocurrency pair to process, e.g., 'ETHUSDT'.")
    parser.add_argument("-operation", type=str, choices=["initialLoad", "updateFuture", "manageHistory"], help="The operation to perform: initialLoad, updateFuture, or manageHistory.")
    parser.add_argument("-limit", type=int, help="Override the limit for data ingestion.")
    parser.add_argument("-testpair", type=str, help="The cryptocurrency pair to test, e.g., '1INCHUSDT'.")

    args = parser.parse_args()

    db_file_path = f"{args.pair}.db"
    db_file_full_path = os.path.join('databases', db_file_path)  # Ensures the DB is created in the databases directory

    pairs_manager = PairsConfigManager('config/pairs.xml')
    data_manager = DataOperationManager('config/pairs.xml')  # Pass configuration file or object

    if args.testpair:
        pairs_manager.check_and_add_pair(args.testpair)
    elif args.operation == "initialLoad" and args.pair:
        limit = args.limit if args.limit else int(data_manager.config.get(args.pair, 'limit'))
        data_manager.perform_initial_load(args.pair, limit, db_file=db_file_full_path)
    else:
        print("Please specify a valid operation and pair.")

if __name__ == '__main__':
    main()
