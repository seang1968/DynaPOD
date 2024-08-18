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
