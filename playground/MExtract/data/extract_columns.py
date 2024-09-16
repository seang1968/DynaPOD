import pandas as pd
import os
import sys

def extract_columns(input_file):
    try:
        # Check if the file exists
        if not os.path.exists(input_file):
            print(f"File not found: {input_file}")
            return None
        
        # Check the file extension to determine how to load the file
        file_extension = os.path.splitext(input_file)[1].lower()

        print(f"Detected file extension: {file_extension}")

        if file_extension == '.csv':
            df = pd.read_csv(input_file)
            print(f"CSV file loaded successfully. Shape: {df.shape}")
        elif file_extension == '.xlsx':
            df = pd.read_excel(input_file)
            print(f"XLSX file loaded successfully. Shape: {df.shape}")
        else:
            print("Unsupported file format. Please provide a CSV or XLSX file.")
            return None

        # Extract column names
        column_names = df.columns.tolist()
        print(f"Extracted column names: {column_names}")

        # Create the output file in the same directory with the original file name but with a .txt extension
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        output_file = os.path.join(os.getcwd(), f"{base_name}_columns.txt")
        print(f"Output file will be created at: {output_file}")
        
        # Write column names to the output file
        with open(output_file, 'w') as f:
            for col in column_names:
                f.write(col + '\n')
                print(f"Written column: {col}")

        print(f"Column names written to file: {output_file}")

        # Return the path of the output file
        return output_file
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    print("Script started")
    if len(sys.argv) != 2:
        print("Usage: python extract_columns.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    print(f"Processing file: {input_file}")
    output_file_path = extract_columns(input_file)
    
    if output_file_path:
        print(f"Column names extracted to file: {output_file_path}")
    else:
        print("Failed to extract column names.")
