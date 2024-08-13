import sys
import shlex

def main_menu():
    print("\nMain Menu:")
    print("1. File Operations")
    print("2. Edit Operations")
    print("3. Help")
    print("4. Exit")
    choice = input("Please choose an option: ")
    return choice

def parse_command(command):
    # Define default values
    defaults = {
        '-file': 'default_file.txt',
        '-resolution': '1920x1080',
        '-n': '1'
    }
    
    args = shlex.split(command)
    params = defaults.copy()  # Start with the defaults
    
    for i, arg in enumerate(args):
        if arg.startswith('-'):
            params[arg] = args[i + 1] if i + 1 < len(args) and not args[i + 1].startswith('-') else None
    
    return params

def file_menu():
    while True:
        print("\nFile Operations Menu:")
        print("1. Open File")
        print("2. Save File")
        print("3. Back to Main Menu")
        command = input("Please choose an option and add parameters (optional): ")
        
        if command.strip():
            parts = command.split(maxsplit=1)
            choice = parts[0]
            additional_params = parts[1] if len(parts) > 1 else ""
        else:
            choice = "3"  # Default to back to main menu
            additional_params = ""

        params = parse_command(additional_params)

        if choice == '1':
            file_name = params['-file']
            resolution = params['-resolution']
            number = params['-n']
            print(f"You chose to Open a File: {file_name} with resolution {resolution} and n = {number}")
        elif choice == '2':
            file_name = params['-file']
            print(f"You chose to Save a File: {file_name}")
        elif choice == '3':
            break  # Exit the file_menu loop and return to the main menu
        else:
            print("Invalid choice. Please try again.")

def edit_menu():
    print("\nEdit Operations Menu:")
    print("1. Copy")
    print("2. Paste")
    print("3. Back to Main Menu")
    choice = input("Please choose an option: ")
    return choice

def help_menu():
    print("\nHelp Menu:")
    print("1. Help with File Operations")
    print("2. Help with Edit Operations")
    print("3. Back to Main Menu")
    choice = input("Please choose an option: ")
    return choice

def display_help(topic):
    if topic == "file":
        print("\nHelp for File Operations:")
        print(" - Open File: Opens a file for reading or writing.")
        print(" - Save File: Saves the current file.")
    elif topic == "edit":
        print("\nHelp for Edit Operations:")
        print(" - Copy: Copies the selected text.")
        print(" - Paste: Pastes the copied text.")
    input("\nPress Enter to return to the Help Menu.")

def main():
    while True:
        choice = main_menu()
        if choice == '1':
            while True:
                file_menu()  # Loop until user selects option 3
                break  # Return to the main menu after exiting file_menu
        elif choice == '2':
            while True:
                edit_choice = edit_menu()
                if edit_choice == '1':
                    print("You chose to Copy.")
                elif edit_choice == '2':
                    print("You chose to Paste.")
                elif edit_choice == '3':
                    break
                else:
                    print("Invalid choice. Please try again.")
        
        elif choice == '3':
            while True:
                help_choice = help_menu()
                if help_choice == '1':
                    display_help("file")
                elif help_choice == '2':
                    display_help("edit")
                elif help_choice == '3':
                    break
                else:
                    print("Invalid choice. Please try again.")
        
        elif choice == '4':
            print("Exiting the application.")
            sys.exit()
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
