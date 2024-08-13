# menu_manager.py
# This class manages the dynamic menu system. It uses the parsed menu structure
# from MenuParser and displays menus and submenus based on user input.

from menu_parser import MenuParser
from operation_manager import OperationManager

class MenuManager:
    def __init__(self, xml_file):
        self.menu_parser = MenuParser(xml_file)  # Initialize the parser with the XML file
        self.menu_structure = self.menu_parser.get_menu_structure()  # Get the parsed menu structure
        self.operation_manager = OperationManager()  # Initialize the operation manager

    def display_menu(self, current_menu=None, level=1):
        # This method displays the current menu and handles user input for navigating submenus or executing actions.
        current_menu = current_menu or self.menu_structure  # Use the main menu structure if no submenu is provided
        while True:
            print("\n" + ">" * (level - 1) + " Menu:")  # Display the menu level
            for index, (menu_item, details) in enumerate(current_menu.items()):
                help_text = details['help']
                print(f"{index + 1}. {menu_item} - {help_text}")  # Show each menu item with its help text
            print(f"{len(current_menu) + 1}. Back to Previous Menu" if level > 1 else f"{len(current_menu) + 1}. Exit")

            try:
                choice = int(input("Please choose an option: ")) - 1  # Get user choice
                if choice == len(current_menu):
                    break  # Return to the previous menu or exit
                
                selected_item = list(current_menu.keys())[choice]
                submenu = current_menu[selected_item].get('submenu')
                if submenu:
                    self.display_menu(submenu, level + 1)  # Recursively display deeper submenus
                else:
                    self.execute_action(selected_item, current_menu[selected_item])
            except (IndexError, ValueError):
                print("Invalid choice. Please try again.")  # Handle invalid input gracefully

    def execute_action(self, operation_name, subitem):
        # This method executes the selected operation by passing it to the OperationManager.
        params = subitem.get('params', {})
        help_text = subitem['help']

        if help_text:
            print(f"\nHelp: {help_text}")  # Display help text before executing the action

        param_values = {}
        for param_name, param_info in params.items():
            value = input(f"Enter {param_name} (default: {param_info['default']}): ") or param_info['default']
            param_values[param_name] = value

        self.operation_manager.execute_operation(operation_name, param_values)  # Execute the operation with parameters
