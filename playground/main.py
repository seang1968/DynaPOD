# main.py
# This is the entry point of the application. It initializes the menu system
# by loading the XML configuration file and then displaying the dynamic menu.

from menu.menu_manager import MenuManager

def main():
    xml_file = 'config/menu_config.xml'  # Path to your XML configuration file
    menu_manager = MenuManager(xml_file)  # Initialize the MenuManager with the XML file

    while True:
        result = menu_manager.display_menu()  # Start the menu system
        if result == "main_menu":
            continue  # If signaled, go back to the main menu
        break  # Exit the loop if there's no signal to continue

if __name__ == "__main__":
    main()  # Call the main function to start the application
