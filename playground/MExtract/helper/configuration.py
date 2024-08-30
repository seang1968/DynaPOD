#configuration.py
import datetime
import json
import xml.etree.ElementTree as ET

class Configuration:
    # Conversion functions for different data types
    CONVERT_FUNC = {
        'integer': int,
        'float': float,
        'boolean': lambda x: x.lower() in ('true', '1'),
        'date': lambda x: datetime.datetime.strptime(x, '%Y-%m-%d').date(),
        'list': json.loads,
        'string': str
    }

    def __init__(self, filename):
        # Initialize with the given XML filename
        self.filename = filename
        # Dictionary to store configuration settings
        self.settings = {}
        # Load configuration from the file
        self.load()

    def load(self):
        """Load settings from the XML configuration file."""
        try:
            self.tree = ET.parse(self.filename)  # Save the tree as an instance attribute
            root = self.tree.getroot()

            # Check if the config is for multiple pairs
            pairs = root.find('pairs')
            if pairs is not None:
                for pair in pairs.findall('pair'):
                    pair_name = pair.get('name')
                    self.settings[pair_name] = {}
                    for setting in pair.findall('setting'):
                        name = setting.get('name')
                        value = setting.get('value')
                        value_type = setting.get('type')
                        self.settings[pair_name][name] = (value, value_type)
            else:
                # Parse each <setting> element in the XML (for single pair or general config)
                for setting in root.findall('setting'):
                    name = setting.get('name')
                    value = setting.get('value')
                    value_type = setting.get('type')
                    self.settings[name] = (value, value_type)
            
            print(f"Configuration loaded: {self.settings}")  # Debugging line

        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file '{self.filename}' not found.")
        except ET.ParseError:
            raise ET.ParseError(f"Failed to parse the configuration file '{self.filename}'.")

    def get(self, pair_name_or_setting_name: str, setting_name: str = None):
        """Retrieve a setting by name, or by pair name and setting name."""
        if setting_name:
            # This means we're retrieving a setting for a specific pair
            if pair_name_or_setting_name in self.settings and setting_name in self.settings[pair_name_or_setting_name]:
                value, value_type = self.settings[pair_name_or_setting_name][setting_name]
                return self.CONVERT_FUNC.get(value_type, str)(value)
            raise KeyError(f"Configuration parameter '{setting_name}' for pair '{pair_name_or_setting_name}' not found")
        else:
            # This means we're retrieving a general setting
            if pair_name_or_setting_name in self.settings:
                value, value_type = self.settings[pair_name_or_setting_name]
                return self.CONVERT_FUNC.get(value_type, str)(value)
            raise KeyError(f"Configuration parameter '{pair_name_or_setting_name}' not found")

    def get_with_default(self, name, default_value, value_type):
        """Retrieve a setting by name with a default value if it does not exist."""
        if name in self.settings:
            value, stored_type = self.settings[name]
            return self.CONVERT_FUNC.get(stored_type, str)(value)
        else:
            # Add the default value to the settings
            self.settings[name] = (default_value, value_type)
            return default_value

    def update_setting(self, name, new_value, value_type):
        """Update an existing setting."""
        if name in self.settings:
            self.settings[name] = (new_value, value_type)
        else:
            raise KeyError(f"Setting '{name}' not found")

    def update_or_create_setting(self, name, new_value, value_type):
        """Update an existing setting or create it if it does not exist."""
        self.settings[name] = (new_value, value_type)

    def delete_setting(self, name):
        """Delete an existing setting."""
        if name in self.settings:
            del self.settings[name]
        else:
            raise KeyError(f"Setting '{name}' not found")
        
    def delete_pair(self, pair_name):
        root = self.tree.getroot()
        for pair in root.findall('pair'):
            if pair.get('name') == pair_name:
                root.remove(pair)
                self.tree.write(self.filename)  # Save changes back to the file
                return True
        return False
    
    def save(self):
        """Save the settings back to the XML configuration file."""
        root = ET.Element("config")
        
        if 'pairs' in self.settings:
            pairs_element = ET.SubElement(root, 'pairs')
            for pair_name, pair_settings in self.settings.items():
                pair_element = ET.SubElement(pairs_element, 'pair', {'name': pair_name})
                for setting_name, (value, value_type) in pair_settings.items():
                    ET.SubElement(pair_element, 'setting', {
                        'name': setting_name,
                        'value': str(value),
                        'type': value_type
                    })
        else:
            for setting_name, (value, value_type) in self.settings.items():
                ET.SubElement(root, 'setting', {
                    'name': setting_name,
                    'value': str(value),
                    'type': value_type
                })
        
        tree = ET.ElementTree(root)
        tree.write(self.filename, encoding='utf-8', xml_declaration=True)
