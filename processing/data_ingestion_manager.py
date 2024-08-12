from database.sqlite_database import SQLiteDatabase
from processing.data_transformer import DataTransformer

class DataIngestionManager:
    def __init__(self, config, data_source, security):
        self.config = config
        self.data_source = data_source
        self.security = security
        self.db = SQLiteDatabase(f"{security}.db", self.security)  # Ensure the security is passed correctly
        self.transformer = DataTransformer(self.config, self.security)

    def get_latest_timestamp(self):
        with self.db.conn as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT MAX(datetime) FROM {self.security}")
            result = cursor.fetchone()
            return result[0] if result[0] is not None else None

    def run(self):
        # Fetch the raw data
        print("Fetching initial data load")
        raw_data = self.data_source.fetch_minute_data()

        # Transform the data
        transformed_data = self.transformer.transform(raw_data)

        # Store the transformed data
        self.db.store_data(transformed_data)
