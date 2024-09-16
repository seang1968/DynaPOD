import sqlite3
from sqlite3 import Error

# Define the database name
DATABASE_NAME = "configurations.db"

# Function to create a connection to the SQLite database
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connected to SQLite: {sqlite3.version}")
    except Error as e:
        print(f"Error creating connection: {e}")
    return conn

# Function to create the tables
def create_tables(conn):
    try:
        cursor = conn.cursor()
        
        # Create Coins table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Coins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                coin_name TEXT NOT NULL UNIQUE
            );
        """)
        
        # Create Channels table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Channels (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                channel_name TEXT NOT NULL UNIQUE
            );
        """)
        
        # Create Markets table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Markets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                market_name TEXT NOT NULL UNIQUE
            );
        """)
        
        conn.commit()
        print("Tables created successfully")
        
    except Error as e:
        print(f"Error creating tables: {e}")

# Function to insert a coin, ensuring uniqueness
def insert_coin(conn, coin_name):
    try:
        cursor = conn.cursor()
        coin_name = coin_name.upper()  # Ensure case insensitivity
        cursor.execute("INSERT OR IGNORE INTO Coins (coin_name) VALUES (?)", (coin_name,))
        conn.commit()
        print(f"Coin '{coin_name}' inserted successfully or already exists")
    except Error as e:
        print(f"Error inserting coin: {e}")

# Function to insert a channel, ensuring uniqueness
def insert_channel(conn, channel_name):
    try:
        cursor = conn.cursor()
        channel_name = channel_name.upper()  # Ensure case insensitivity
        cursor.execute("INSERT OR IGNORE INTO Channels (channel_name) VALUES (?)", (channel_name,))
        conn.commit()
        print(f"Channel '{channel_name}' inserted successfully or already exists")
    except Error as e:
        print(f"Error inserting channel: {e}")

# Function to insert a market, ensuring uniqueness
def insert_market(conn, market_name):
    try:
        cursor = conn.cursor()
        market_name = market_name.upper()  # Ensure case insensitivity
        cursor.execute("INSERT OR IGNORE INTO Markets (market_name) VALUES (?)", (market_name,))
        conn.commit()
        print(f"Market '{market_name}' inserted successfully or already exists")
    except Error as e:
        print(f"Error inserting market: {e}")

# Main function to create database and insert example data
def main():
    # Create a database connection
    conn = create_connection(DATABASE_NAME)
    
    if conn:
        # Create tables
        create_tables(conn)
        
        # Example data
        coins = ['BTC', 'ETH', 'XRP']
        channels = ['TradingChannel1', 'NewsChannel1', 'PriceAlerts']
        markets = ['Binance', 'Coinbase', 'Kraken']
        
        # Insert example data
        for coin in coins:
            insert_coin(conn, coin)
        
        for channel in channels:
            insert_channel(conn, channel)
        
        for market in markets:
            insert_market(conn, market)
        
        # Close the connection
        conn.close()

if __name__ == '__main__':
    main()
