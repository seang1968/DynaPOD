#main.py
from menu_manager import MenuManager

def main():
    xml_file = 'menu_config.xml'  # Path to your XML configuration file
    menu_manager = MenuManager(xml_file)
    menu_manager.display_menu()

if __name__ == "__main__":
    main()
