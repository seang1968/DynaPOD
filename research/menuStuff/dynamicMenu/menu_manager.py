#menu_manager.py
from menu_parser import MenuParser
from operation_manager import OperationManager

class MenuManager:
    def __init__(self, xml_file):
        self.menu_parser = MenuParser(xml_file)
        self.menu_structure = self.menu_parser.get_menu_structure()
        self.operation_manager = OperationManager()

    def display_menu(self):
        while True:
            for index, menu_item in enumerate(self.menu_structure.keys()):
                print(f"{index + 1}. {menu_item}")
            print(f"{len(self.menu_structure) + 1}. Exit")

            choice = int(input("Please choose an option: ")) - 1

            if choice == len(self.menu_structure):
                print("Exiting the application.")
                break

            selected_menu = list(self.menu_structure.keys())[choice]
            submenu_items = self.menu_structure[selected_menu]

            if submenu_items:
                self.display_submenu(selected_menu, submenu_items)

    def display_submenu(self, menu_name, submenu_items):
        while True:
            print(f"\n{menu_name}:")
            for index, subitem in enumerate(submenu_items):
                print(f"{index + 1}. {subitem['name']}")
            print(f"{len(submenu_items) + 1}. Back to Main Menu")

            choice = int(input("Please choose an option: ")) - 1

            if choice == len(submenu_items):
                break

            selected_subitem = submenu_items[choice]
            self.execute_action(selected_subitem)

    def execute_action(self, subitem):
        params = subitem['params']
        help_text = subitem['help']

        if help_text:
            print(f"\nHelp: {help_text}")

        param_values = {}
        for param_name, param_info in params.items():
            value = input(f"Enter {param_name} (default: {param_info['default']}): ") or param_info['default']
            param_values[param_name] = value

        self.operation_manager.execute_operation(subitem['name'], param_values)
