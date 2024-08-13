#data_ingestion_manager.py
from database.sqlite_database import SQLiteDatabase
from processing.data_transformer import DataTransformer

class DataIngestionManager:
    def __init__(self, config, data_source, security):
        self.config = config
        self.data_source = data_source
        self.security = security
        self.db = SQLiteDatabase(f"databases/{security}.db")  # Ensure the DB is created in the databases directory

    def run(self, limit):
        raw_data = self.data_source.fetch_minute_data(limit)
        transformed_data = self.transformer.transform(raw_data)
        self.db.store_data(transformed_data)
        self.db.close()

    def get_latest_timestamp(self):
        with self.db.conn as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT MAX(datetime) FROM {self.security}")
            result = cursor.fetchone()
            return result[0] if result[0] is not None else None
        
    # def run(self, limit=None):
    #     # Fetch the raw data with an optional limit
    #     print("Fetching initial data load")
    #     if limit:
    #         raw_data = self.data_source.fetch_minute_data(limit)
    #     else:
    #         raw_data = self.data_source.fetch_minute_data()

    #     # Transform the data
    #     transformed_data = self.transformer.transform(raw_data)

    #     # Store the transformed data
    #     self.db.store_data(transformed_data)    