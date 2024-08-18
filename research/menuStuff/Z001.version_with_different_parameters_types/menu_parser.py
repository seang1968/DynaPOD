import xml.etree.ElementTree as ET

class MenuParser:
    def __init__(self, xml_file):
        self.xml_file = xml_file
        self.menu_structure = self.parse_menu_config()

    def parse_menu_config(self):
        tree = ET.parse(self.xml_file)
        root = tree.getroot()
        return self._parse_menu_items(root)

    def _parse_menu_items(self, root):
        menu_structure = {}

        for item in root:
            if item.tag == 'menu' or item.tag == 'item':  # Handle both 'menu' and 'item' tags
                name = item.get('name')
                help_text = item.find('help').text if item.find('help') is not None else ''
                submenu = item.find('submenu')

                if submenu:
                    submenu_items = self._parse_menu_items(submenu)
                    menu_structure[name] = {
                        'help': help_text,
                        'submenu': submenu_items,
                        'type': item.tag  # Store whether it's a 'menu' or 'item'
                    }
                else:
                    params = {}
                    for param in item.findall('param'):
                        param_name = param.get('name')
                        default = param.get('default')
                        param_type = param.get('type')
                        params[param_name] = {'default': default, 'type': param_type}

                    menu_structure[name] = {
                        'help': help_text,
                        'params': params,
                        'type': item.tag  # Store whether it's a 'menu' or 'item'
                    }

        return menu_structure

    def get_menu_structure(self):
        return self.menu_structure  # Provide access to the parsed menu structure
