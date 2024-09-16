import sqlite3
import sys
from sqlite3 import Error

def create_connection(db_file):
    """ Create a database connection to the SQLite database specified by db_file """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connected to SQLite: {sqlite3.version}")
        return conn
    except Error as e:
        print(f"Error creating connection: {e}")
    return conn

def generate_db_info(conn, output_file, db_file):
    """ Generate a document with information about the database schema """
    try:
        cursor = conn.cursor()
           
        # Get the list of tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        with open(output_file, 'w') as f:
            f.write(f"Database File Path: {db_file}\n")
            f.write(f"Database Configuration and Information\n")
            f.write(f"====================================\n\n")
            f.write(f"Database File: {conn}\n")
            f.write(f"SQLite Version: {sqlite3.version}\n\n")
            f.write(f"Tables:\n")
            f.write(f"-------\n")
            
            for table_name in tables:
                f.write(f"Table: {table_name[0]}\n")
                
                # Get the table schema
                cursor.execute(f"PRAGMA table_info({table_name[0]})")
                columns = cursor.fetchall()
                
                f.write(f"Columns:\n")
                for column in columns:
                    f.write(f"  {column[1]} ({column[2]})\n")
                f.write(f"\n")
                
        print(f"Database information has been written to {output_file}")
        
    except Error as e:
        print(f"Error generating database info: {e}")

def main(db_file):
    # Generate the output file name
    output_file = f"{db_file}_info.txt"
    
    # Create a database connection
    conn = create_connection(db_file)
    print (db_file)
    if conn:
        # Generate the database information
        generate_db_info(conn, output_file, db_file)
        
        # Close the connection
        conn.close()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python generate_db_info.py <database_name>")
    else:
        db_file = sys.argv[1]
        main(db_file)
