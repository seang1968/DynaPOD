import os
import json  # Required to handle list and map parameters
from menu_parser import MenuParser
from operation_manager import OperationManager

class MenuManager:
    def __init__(self, xml_file):
        self.menu_parser = MenuParser(xml_file)  # Initialize the parser with the XML file
        self.menu_structure = self.menu_parser.get_menu_structure()  # Get the parsed menu structure
        self.operation_manager = OperationManager()  # Initialize the operation manager

    def clear_terminal(self):
        # Clears the terminal screen for a cleaner display
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_menu(self, current_menu=None, level=1, parent_name="Main Menu", parent_help=None):
        current_menu = current_menu or self.menu_structure  # Use the main menu structure if no submenu is provided

        while True:
            # Set help text for the main menu or any submenu
            if level == 1:
                parent_help = "This is the main menu of the application."  # Set the help text for the main menu
            elif parent_help is None:
                parent_help = current_menu.get('help', '')

            self.clear_terminal()  # Clear the terminal before showing the menu
            self.show_menu(parent_name, parent_help, current_menu, level)  # Show the menu with the help text

            try:
                choice = int(input("Please choose an option: ")) - 1  # Get user choice
                if choice == len(current_menu):
                    if level == 1:
                        return  # Exit the main menu loop
                    else:
                        return  # Go back to the previous menu
                
                selected_item = list(current_menu.keys())[choice]
                submenu = current_menu[selected_item].get('submenu')
                selected_help = current_menu[selected_item].get('help', '')
                
                if submenu:
                    # If it's a submenu, display the menu name and help text before diving deeper
                    self.display_menu(submenu, level + 1, selected_item, selected_help)  # Recursively display deeper submenus
                else:
                    self.execute_action(selected_item, current_menu[selected_item])
            except (IndexError, ValueError):
                print("Invalid choice. Please try again.")  # Handle invalid input gracefully

    def show_menu(self, name, help_text, menu, level):
        """Display the menu with the provided name and help text."""
        print(f"{name}")  # Display the name of the current menu
        if help_text:
            print(f"Help: {help_text}")  # Display the help text for the current menu

        print("\n" + ">" * (level - 1) + f" {name}:")  # Display the menu level with the specific name
        # Enumerate through menu items
        item_keys = [key for key in menu.keys() if isinstance(menu[key], dict)]
        for index, menu_item in enumerate(item_keys):
            details = menu[menu_item]
            help_text = details.get('help', '')
            print(f"{index + 1}. {menu_item} - {help_text}")  # Show each menu item with its help text
        print(f"{len(item_keys) + 1}. Back to Previous Menu" if level > 1 else f"{len(item_keys) + 1}. Exit")

    def execute_action(self, operation_name, subitem):
        params = subitem.get('params', {})
        help_text = subitem.get('help')

        if help_text:
            print(f"\nHelp: {help_text}")  # Display help text before executing the action

        param_values = {}
        for param_name, param_info in params.items():
            value = input(f"Enter {param_name} (default: {param_info['default']}): ") or param_info['default']
            # Type casting based on the 'type' attribute
            if param_info['type'] == 'int':
                try:
                    value = int(value)
                except ValueError:
                    print(f"Invalid input for {param_name}. Expected an integer. Using default value {param_info['default']}.")
                    value = int(param_info['default'])
            elif param_info['type'] == 'float':
                try:
                    value = float(value)
                except ValueError:
                    print(f"Invalid input for {param_name}. Expected a float. Using default value {param_info['default']}.")
                    value = float(param_info['default'])
            elif param_info['type'] == 'bool':
                value = value.lower() in ['true', '1', 'yes']
            elif param_info['type'] == 'list':
                try:
                    value = json.loads(value)
                    if not isinstance(value, list):
                        raise ValueError
                except ValueError:
                    print(f"Invalid input for {param_name}. Expected a list. Using default value.")
                    value = json.loads(param_info['default'])
            elif param_info['type'] == 'map':
                try:
                    value = json.loads(value)
                    if not isinstance(value, dict):
                        raise ValueError
                except ValueError:
                    print(f"Invalid input for {param_name}. Expected a map. Using default value.")
                    value = json.loads(param_info['default'])
            # For 'str', no casting is needed
            param_values[param_name] = value

        self.operation_manager.execute_operation(operation_name, param_values)  # Execute the operation with parameters
