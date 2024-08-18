# action_handler.py
# This class is responsible for handling specific actions that can be triggered from the menu system.
# It contains methods that correspond to menu items, which can accept parameters and perform actions.
from CITI.md_aws_bucket import MarkdownS3Processor  # Import the MarkdownS3Processor class
class ActionHandler:
    def __init__(self):
        pass  # Constructor can be used to initialize any required state

    def dummy_action(self, param1, param2):
        # This is a dummy method that simulates an action being performed with two parameters.
        print(f"Dummy action performed with param1='{param1}' and param2='{param2}'")
        # Here you can add the actual logic for the dummy action

    def data_types_example(self, integer_param, float_param, boolean_param, list_param, map_param):
        # Example method to demonstrate handling different data types
        print(f"Integer: {integer_param}")
        print(f"Float: {float_param}")
        print(f"Boolean: {boolean_param}")
        print(f"List: {list_param}")
        print(f"Map: {map_param}")
        # Here you can add the actual logic for handling these data types
    def run_citi_aws_bucket_job(self, md_source="clipboard", bucket_name="sean-site-bucket"):
        # Create an instance of MarkdownS3Processor with the given parameters
        processor = MarkdownS3Processor(md_source=md_source, bucket_name=bucket_name)
        processor.test_proess_clipboard()  # Run the process using clipboard by default