import sys
import pyperclip

def process_symbols(file_name):
    try:
        # Read the file and split lines by commas
        with open(file_name, 'r') as f:
            data = f.read()

        # Debug: Print raw data read from the file
        print("Raw data from file:", data)

        # Split the string into a list of elements
        symbols_list = data.strip().split(',')

        # Debug: Print the list of symbols after splitting
        print("Split symbols list:", symbols_list)

        # Process each element to remove market name and USDT.P suffix
        processed_symbols = []
        for symbol in symbols_list:
            parts = symbol.split(':')
            if len(parts) > 1:
                clean_symbol = parts[1].replace('USDT.P', '').replace('USDT', '').strip()
                processed_symbols.append(clean_symbol)
            else:
                # Debug: Print symbols that don't match the expected format
                print(f"Skipping symbol (unexpected format): {symbol}")

        # Debug: Print the processed symbols before formatting the output
        print("Processed symbols:", processed_symbols)

        # Format the output to look like the coin suggestions list
        output = 'self.coin_suggestions = [\n'
        for i, symbol in enumerate(processed_symbols):
            if i % 5 == 0 and i > 0:
                output += '\n'  # Create a new line every 5 items for readability
            output += f'    "{symbol}", '
        output += '\n]'

        # Print the formatted output
        print(output)

        # Ensure the entire output is copied to the clipboard
        pyperclip.copy(output)  # Copy the output string to the clipboard

        # Debug: Print confirmation of copying to clipboard
        print("\nThe formatted output has been copied to the clipboard.")

    except FileNotFoundError:
        print(f"File '{file_name}' not found.")

if __name__ == "__main__":
    # Ensure the user passes the file name as an argument
    if len(sys.argv) < 2:
        print("Please provide the file name as an argument.")
    else:
        # Process the file passed as a command-line argument
        file_name = sys.argv[1]
        process_symbols(file_name)
