#pairs_config_manager.py
import xml.etree.ElementTree as ET
from data_source.binance_data_source import BinanceDataSource
from config.configuration import Configuration

class PairsConfigManager:
    def __init__(self, config_file: str):
        self.config_file = config_file
        self.config = Configuration(config_file)
    
    def add_pair_to_config(self, pair_name: str):
        tree = ET.parse(self.config_file)
        root = tree.getroot()

        # Navigate to the <pairs> element within <config>
        pairs_element = root.find('pairs')
        if pairs_element is None:
            raise ValueError("The configuration file does not have a <pairs> element under the <config> root.")

        # Check if the pair already exists
        pair_exists_in_config = any(pair.get('name') == pair_name for pair in pairs_element.findall('pair'))

        if not pair_exists_in_config:
            new_pair = ET.Element('pair', {'name': pair_name})
            
            settings = [
                {'name': 'time_frame', 'type': 'string', 'value': '1m'},
                {'name': 'limit', 'type': 'integer', 'value': '1000'},
                {'name': 'db_file', 'type': 'string', 'value': f'{pair_name}.db'},
                {'name': 'timezone', 'type': 'string', 'value': 'America/New_York'}
            ]
            
            for setting in settings:
                ET.SubElement(new_pair, 'setting', setting)
            
            pairs_element.append(new_pair)  # Append new pair inside the <pairs> tag
            tree.write(self.config_file)
            print(f"Added {pair_name} to {self.config_file}")
            return True
        else:
            print(f"{pair_name} already exists in {self.config_file}")
            return True

    def check_and_add_pair(self, pair_name: str):
        data_source = BinanceDataSource(pair_name=pair_name)
        if data_source.pair_exists():
            print(f"The pair {pair_name} is available on Binance.")
            return self.add_pair_to_config(pair_name)
        else:
            print(f"The pair {pair_name} is NOT available on Binance.")
            return False
