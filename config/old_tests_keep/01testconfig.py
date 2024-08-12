# test_configuration.py

import os
from config.configuration import Configuration


# Path to the test configuration file
test_config_file = 'test_config.xml'

# Helper function to create a fresh test XML file
def create_test_xml():
    with open(test_config_file, 'w') as f:
        f.write('''<config>
    <setting name="coin_pair" type="string" value="BTCUSDT" />
    <setting name="time_frame" type="string" value="1m" />
    <setting name="limit" type="integer" value="100" />
    <setting name="timezone" type="string" value="America/New_York" />
</config>''')

# Create the test XML file
create_test_xml()

# Instantiate the Configuration class with the test file
config = Configuration(test_config_file)

# Test loading of configurations
def test_loading():
    print("\n--- Testing Loading ---")
    try:
        assert config.get('coin_pair') == "BTCUSDT"
        assert config.get('time_frame') == "1m"
        assert config.get('limit') == 100
        assert config.get('timezone') == "America/New_York"
        print("Loading Test Passed")
    except AssertionError as e:
        print(f"Loading Test Failed: {e}")

# Test retrieval of settings with default
def test_get_with_default():
    print("\n--- Testing Get with Default ---")
    try:
        assert config.get_with_default('non_existing_setting', "default_value", 'string') == "default_value"
        assert config.get('non_existing_setting') == "default_value"  # Check if it was added
        print("Get with Default Test Passed")
    except AssertionError as e:
        print(f"Get with Default Test Failed: {e}")

# Test updating an existing setting
def test_update_setting():
    print("\n--- Testing Update Setting ---")
    try:
        config.update_setting('coin_pair', 'ETHUSDT', 'string')
        assert config.get('coin_pair') == "ETHUSDT"
        print("Update Setting Test Passed")
    except AssertionError as e:
        print(f"Update Setting Test Failed: {e}")

# Test adding a new setting
def test_update_or_create_setting():
    print("\n--- Testing Update or Create Setting ---")
    try:
        config.update_or_create_setting('new_setting', 'new_value', 'string')
        assert config.get('new_setting') == "new_value"
        print("Update or Create Setting Test Passed")
    except AssertionError as e:
        print(f"Update or Create Setting Test Failed: {e}")

# Test deleting a setting
def test_delete_setting():
    print("\n--- Testing Delete Setting ---")
    try:
        config.delete_setting('new_setting')
        try:
            config.get('new_setting')
            print("Delete Setting Test Failed: Setting was not deleted")
        except KeyError:
            print("Delete Setting Test Passed")
    except KeyError as e:
        print(f"Delete Setting Test Failed: {e}")

# Run the tests
if __name__ == "__main__":
    test_loading()
    test_get_with_default()
    test_update_setting()
    test_update_or_create_setting()
    test_delete_setting()

    # Clean up the test file
    os.remove(test_config_file)
