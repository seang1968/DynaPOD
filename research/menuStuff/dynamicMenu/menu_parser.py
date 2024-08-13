#menu_parser.py
import xml.etree.ElementTree as ET

class MenuParser:
    def __init__(self, xml_file):
        self.xml_file = xml_file
        self.menu_structure = self.parse_menu_config()

    def parse_menu_config(self):
        tree = ET.parse(self.xml_file)
        root = tree.getroot()
        
        menu_structure = {}
        
        for item in root.findall('item'):
            name = item.get('name')
            menu_structure[name] = []
            submenu = item.find('submenu')
            
            if submenu:
                for subitem in submenu.findall('item'):
                    sub_name = subitem.get('name')
                    params = {}
                    for param in subitem.findall('param'):
                        param_name = param.get('name')
                        default = param.get('default')
                        param_type = param.get('type')
                        params[param_name] = {'default': default, 'type': param_type}
                    
                    help_text = subitem.find('help').text if subitem.find('help') is not None else ''
                    menu_structure[name].append({
                        'name': sub_name,
                        'params': params,
                        'help': help_text
                    })
        
        return menu_structure

    def get_menu_structure(self):
        return self.menu_structure
