# main.py
# This is the entry point of the application. It initializes the menu system
# by loading the XML configuration file and then displaying the dynamic menu.

from menu_manager import MenuManager

def main():
    xml_file = 'menu_config.xml'  # Path to your XML configuration file
    menu_manager = MenuManager(xml_file)  # Initialize the MenuManager with the XML file
    menu_manager.display_menu()  # Start the menu system

if __name__ == "__main__":
    main()  # Call the main function to start the application
