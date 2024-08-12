# processing/data_ingestion_manager.py

from config.configuration import Configuration
from data_source.binance_data_source import BinanceDataSource
from database.sqlite_database import SQLiteDatabase
from processing.data_transformer import DataTransformer

class DataIngestionManager:
    def __init__(self, config: Configuration, data_source: BinanceDataSource, security: str):
        self.config = config
        self.data_source = data_source
        self.security = security
        self.db = SQLiteDatabase(security)
        self.transformer = DataTransformer(self.config, self.security)

    def run(self):
        raw_data = self.data_source.fetch_minute_data()
        transformed_data = self.transformer.transform(raw_data)
        self.db.store_price_data(transformed_data, self.security)
        self.db.close()
