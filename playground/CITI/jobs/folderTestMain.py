from core.resource_manager import ResourceManager
from xml_consumer import XMLConsumer
import os
import sys

def main(config_file):
    # Initialize the ResourceManager and load resources from the XML
    resource_manager = ResourceManager()
    
    # Load the resources from the configuration XML
    xml_consumer = XMLConsumer(config_file)
    xml_consumer.parse_and_process()

    # Get the folder path from the ResourceManager
    folder_path = resource_manager.get_resource("DataFolder")
    
    # Verify the folder exists
    if os.path.exists(folder_path):
        print(f"Folder exists at: {folder_path}")
    else:
        print(f"Folder was not created correctly at: {folder_path}")
        return

    # Write a test file in the folder
    test_file_path = os.path.join(folder_path, 'test_file.txt')
    with open(test_file_path, 'w') as f:
        f.write("This is a test file inside the folder resource.")
    print(f"Test file created at: {test_file_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <config.xml>")
    else:
        main(sys.argv[1])
