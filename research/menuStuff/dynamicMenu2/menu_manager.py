#menu_manager.py
from menu_parser import MenuParser
from operation_manager import OperationManager

class MenuManager:
    def __init__(self, xml_file):
        self.menu_parser = MenuParser(xml_file)
        self.menu_structure = self.menu_parser.get_menu_structure()
        self.operation_manager = OperationManager()

    def display_menu(self, current_menu=None, level=1):
        current_menu = current_menu or self.menu_structure
        while True:
            print("\n" + ">" * (level - 1) + " Menu:")
            for index, (menu_item, details) in enumerate(current_menu.items()):
                help_text = details['help']
                print(f"{index + 1}. {menu_item} - {help_text}")
            print(f"{len(current_menu) + 1}. Back to Previous Menu" if level > 1 else f"{len(current_menu) + 1}. Exit")

            choice = int(input("Please choose an option: ")) - 1

            if choice == len(current_menu):
                break  # Return to the previous menu or exit

            selected_item = list(current_menu.keys())[choice]
            submenu = current_menu[selected_item].get('submenu')
            if submenu:
                self.display_menu(submenu, level + 1)  # Recursively display deeper submenus
            else:
                self.execute_action(selected_item, current_menu[selected_item])

    def execute_action(self, operation_name, subitem):
        params = subitem.get('params', {})
        help_text = subitem['help']

        if help_text:
            print(f"\nHelp: {help_text}")

        param_values = {}
        for param_name, param_info in params.items():
            value = input(f"Enter {param_name} (default: {param_info['default']}): ") or param_info['default']
            param_values[param_name] = value

        self.operation_manager.execute_operation(operation_name, param_values)
