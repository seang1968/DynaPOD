---

# Dynamic Menu System Documentation

This documentation provides a comprehensive overview of the dynamic menu system, including detailed inline comments in the code files, explanations of the program flow, and guidelines for usage and maintenance. The system is designed to be flexible and easily extendable, allowing you to manage multi-level menus through an XML configuration file.

---

## Table of Contents

1. [Code Files with Inline Comments](#code-files-with-inline-comments)
    - [main.py](#mainpy)
    - [menu_parser.py](#menu_parserpy)
    - [menu_manager.py](#menu_managerpy)
    - [operation_manager.py](#operation_managerpy)
    - [action_handler.py](#action_handlerpy)
    - [menu_config.xml](#menu_configxml)
2. [Program Flow](#program-flow)
3. [External Documentation](#external-documentation)
    - [Overview](#overview)
    - [How to Use](#how-to-use)
    - [Extending the System](#extending-the-system)
    - [Maintenance Tips](#maintenance-tips)
4. [Summary](#summary)

---

## Code Files with Inline Comments

### main.py

```python
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
```

### menu_parser.py

```python
# menu_parser.py
# This class is responsible for parsing the XML configuration file
# and converting it into a Python dictionary structure that represents the menu.

import xml.etree.ElementTree as ET

class MenuParser:
    def __init__(self, xml_file):
        self.xml_file = xml_file  # Path to the XML configuration file
        self.menu_structure = self.parse_menu_config()  # Parse the XML file on initialization

    def parse_menu_config(self):
        # This method parses the XML file and returns a nested dictionary structure.
        tree = ET.parse(self.xml_file)
        root = tree.getroot()
        
        return self._parse_menu_items(root)  # Delegate the parsing to a helper method

    def _parse_menu_items(self, root):
        # This recursive method walks through the XML elements and builds the dictionary structure.
        menu_structure = {}
        
        for item in root.findall('item'):
            name = item.get('name')  # Get the name of the menu item
            help_text = item.find('help').text if item.find('help') is not None else ''  # Get the help text
            submenu = item.find('submenu')
            
            if submenu:
                # If a submenu exists, recursively parse it and store it under the current item
                submenu_items = self._parse_menu_items(submenu)
                menu_structure[name] = {
                    'help': help_text,
                    'submenu': submenu_items
                }
            else:
                # If no submenu exists, collect the parameters and store them
                params = {}
                for param in item.findall('param'):
                    param_name = param.get('name')
                    default = param.get('default')
                    param_type = param.get('type')
                    params[param_name] = {'default': default, 'type': param_type}
                
                menu_structure[name] = {
                    'help': help_text,
                    'params': params
                }
        
        return menu_structure  # Return the built menu structure

    def get_menu_structure(self):
        return self.menu_structure  # Provide access to the parsed menu structure
```

### menu_manager.py

```python
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
            # For 'str', no casting is needed
            param_values[param_name] = value

        self.operation_manager.execute_operation(operation_name, param_values)  # Execute the operation with parameters
```

### operation_manager.py

```python
# operation_manager.py
# This class is responsible for executing operations based on the user's selection.
# It uses method names derived from the operation names defined in the XML file.
# It also delegates specific actions to the ActionHandler class when appropriate.

from action_handler import ActionHandler  # Import the ActionHandler class

class OperationManager:
    def __init__(self):
        self.action_handler = ActionHandler()  # Initialize the ActionHandler

    def execute_operation(self, operation_name, params):
        # This method converts the operation name to a method name by replacing spaces with underscores
        # and converting to lowercase. It then checks if the method exists in ActionHandler or in itself
        # and calls it with the parameters.
        method_name = operation_name.replace(' ', '_').lower()
        if hasattr(self.action_handler, method_name):
            method = getattr(self.action_handler, method_name)
            method(**params)  # Call the method on the ActionHandler with the parameters
        elif hasattr(self, method_name):
            method = getattr(self, method_name)
            method(**params)  # Call the method in OperationManager with the parameters
        else:
            print(f"Operation '{operation_name}' is not implemented.")  # Handle cases where the method is not found

    # Example operation methods that could be called based on user selection

    def open_file(self, file, mode='r'):
        print(f"Opening file '{file}' in mode '{mode}'")
        # Here you can add the actual logic to open the file

    def save_file(self, file):
        print(f"Saving file '{file}'")
        # Here you can add the actual logic to save the file

    def change_resolution(self, resolution):
        print(f"Changing resolution to {resolution}")
        # Here you can add the actual logic to change the resolution

    def set_default_file_name(self, filename):
        print(f"Setting default file name to {filename}")
        # Here you can add the actual logic to set the default file name
```

### action_handler.py

```python
# action_handler.py
# This class is responsible for handling specific actions that can be triggered from the menu system.
# It contains methods that correspond to menu items, which can accept parameters and perform actions.

class ActionHandler:
    def __init__(self):
        pass  # Constructor can be used to initialize any required state

    def dummy_action(self, param1, param2):
        # This is a dummy method that simulates an action being performed with two parameters.
        print(f"Dummy action performed with param1='{param1}' and param2='{param2}'")
        # Here you can add the actual logic for the dummy action
```

### menu_config.xml

```xml
<!-- menu_config.xml -->
<!--
    This XML file defines the structure of the dynamic menu system.
    Each <item> represents a menu option, which may contain parameters, help text, and nested submenus.
    This file can be modified to add, remove, or change menu options without changing the codebase.
-->

<menu>
    <item name="File Operations">
        <help>Operations related to file handling.</help>
        <submenu>
            <item name="Open File">
                <param name="file" default="default.txt" type="str"/>
                <param name="mode" default="r" type="str"/>
                <help>Opens a file with the given name and mode.</help>
            </item>
            <item name="Save File">
                <param name="file" default="output.txt" type="str"/>
                <help>Saves the file with the given name.</help>
            </item>
        </submenu>
    </item>
    <item name="Settings">
        <help>Settings for the application.</help>
        <submenu>
            <item name="Perform Dummy Action">
                <param name="param1" default="default1" type="str"/>
                <param name="param2" default="default2" type="str"/>
                <help>Performs a dummy action with two parameters.</help>
            </item>
            <item name="Display Settings">
                <help>Adjust display-related settings.</help>
                <submenu>
                    <item name="Change Resolution">
                        <param name="resolution" default="1920x1080" type="str"/>
                        <help>Changes the display resolution.</help>
                    </item>
                    <item name="Advanced Display Settings">
                        <help>Advanced options for display settings.</help>
                        <submenu>
                            <item name="Color Calibration">
                                <param name="calibration_value" default="default" type="str"/>
                                <help>Calibrates the display colors.</help>
                            </item>
                            <item name="Brightness Control">
                                <param name="level" default="50" type="int"/>
                                <help>Controls the brightness level.</help>
                            </item>
                        </submenu>
                    </item>
                </submenu>
            </item>
            <item name="Set Default File Name">
                <param name="filename" default="default.txt" type="str"/>
                <help>Sets the default file name used in file operations.</help>
            </item>
        </submenu>
    </item>
</menu>
```

---

## Program Flow

Here's a step-by-step flow of how the program works:

1. **Initialization**:
   - The `main.py` script is the entry point. It initializes the `MenuManager` with the path to the `menu_config.xml` file.
   - `MenuManager` initializes a `MenuParser` to parse the XML file into a nested dictionary structure (`menu_structure`).
   - `MenuManager` also initializes an `OperationManager` to handle the execution of operations, which may delegate certain actions to the `ActionHandler` class.

2. **Displaying the Menu**:
   - The `MenuManager` begins displaying the main menu using the parsed structure.
   - Each menu item displays its help text alongside the option number.
   - The user selects an option by entering the corresponding number.

3. **Handling Submenus**:
   - If the selected item has a submenu, `MenuManager` recursively calls `display_menu` to show the submenu.
   - The user can navigate deeper into submenus or return to the previous menu.

4. **Executing Operations**:
   - If the selected item is an operation (i.e., it has parameters but no submenu), `MenuManager` collects the required parameters from the user.
   - The system handles type casting of the input based on the 'type' attribute specified in the XML.
   - The operation name and parameters are passed to `OperationManager`, which executes the corresponding method or delegates to `ActionHandler`.

5. **Error Handling**:
   - If the user enters an invalid option, `MenuManager` catches the error and prompts the user to try again without crashing the program.
   - During parameter input, if the user provides invalid input that doesn't match the expected type, the system uses the default value and informs the user.

---

## External Documentation

### Overview

This dynamic menu system allows you to create and manage multi-level menus through an XML configuration file. The system is designed to be flexible, allowing you to add, remove, or modify menu items without changing the underlying code. Each menu item can be associated with parameters and actions, which are handled by corresponding classes.

### How to Use

1. **Add or Modify Menus**:
   - Edit the `menu_config.xml` file to define new menus, submenus, and operations.
   - Each `<item>` tag represents a menu item, which can contain parameters (`<param>`) and help text (`<help>`).
   - Nested `<submenu>` tags allow you to create multi-level menus.

2. **Run the Application**:
   - Ensure all the `.py` files and the `menu_config.xml` are in the same directory.
   - Execute `python main.py` to start the menu system.
   - Navigate through the menus by entering the corresponding numbers.
   - Follow the prompts to provide any required parameters for operations.

3. **Provide Input for Parameters**:
   - When prompted for parameters, enter the value as per the expected type (e.g., integer, float, string).
   - If invalid input is provided, the system will notify you and use the default value specified in the XML.

### Extending the System

1. **Adding New Operations**:
   - To add new operations, define corresponding methods in the `OperationManager` class or in the `ActionHandler` class if the action is specific.
   - The method name should match the operation name in the XML file, with spaces replaced by underscores and converted to lowercase.

2. **Example: Dummy Action**:
   - **Action Handler**:
     The `ActionHandler` class in `action_handler.py` contains a method `dummy_action` that is connected to the "Perform Dummy Action" menu item in `menu_config.xml`. This method takes two parameters (`param1` and `param2`) and prints them out to simulate an action.

   - **XML Configuration**:
     ```xml
     <item name="Perform Dummy Action">
         <param name="param1" default="default1" type="str"/>
         <param name="param2" default="default2" type="str"/>
         <help>Performs a dummy action with two parameters.</help>
     </item>
     ```

   - **Integration**:
     The `OperationManager` class is responsible for delegating this action to the `ActionHandler`. When the user selects "Perform Dummy Action" from the menu, the system will prompt the user to enter `param1` and `param2`. The values are then passed to `ActionHandler.dummy_action`, which prints them out.

3. **Type Casting for Parameters**:
   - The system supports type casting for parameters based on the 'type' attribute in the XML (`int`, `float`, `str`).
   - Ensure that the user inputs match the expected types to avoid errors.

### Maintenance Tips

- **Keep XML Organized**: As the menu structure grows, maintain a clear and organized XML file. Use indentation and comments to make it easier to navigate.

- **Error Handling**: Ensure that new methods in `OperationManager` or `ActionHandler` handle unexpected inputs gracefully.

- **Testing**: Regularly test the application after making changes to the XML file or code to ensure everything works as expected.

- **Extensibility**: When adding new features or actions, consider whether they should be placed in `OperationManager` or a specialized handler like `ActionHandler` for better organization.

- **Documentation**: Keep the code well-documented with inline comments to make future maintenance easier.

---

## Summary

With this comprehensive documentation, including detailed code files with inline comments, explanations of program flow, and guidelines for usage and maintenance, you should be well-equipped to maintain and extend this dynamic menu system. The XML configuration allows for flexible updates, and the Python classes handle the parsing, display, and execution of operations in a structured and maintainable way. The addition of the `ActionHandler` class demonstrates how to integrate specific actions seamlessly into the system.

---