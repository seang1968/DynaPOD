import xml.etree.ElementTree as ET
from core.resource_manager import ResourceManager
from core.action_executor import ActionExecutor  # Import ActionExecutor

class XMLConsumer:
    def __init__(self, config_file):
        self.config_file = config_file
        self.resource_manager = ResourceManager()
        self.action_executor = ActionExecutor()  # Create an instance of ActionExecutor

    def parse_and_process(self):
        tree = ET.parse(self.config_file)
        root = tree.getroot()

        # Load resources first (logging should be initialized early)
        resources = root.find('resources')
        if resources:
            self._load_resources(resources)

        # Now execute actions
        actions = root.find('actions')
        if actions:
            self._execute_actions(actions)

    def _load_resources(self, resources):
        for resource in resources.findall('resource'):
            self.resource_manager.load_resource(resource)

    def _execute_actions(self, actions):
        logger = ResourceManager.get_resource("LogFile")  # Get the logger
        logger.info("Starting to execute actions")

        for action in actions.findall('action'):
            logger.debug(f"Executing action: {action.attrib['name']}")
            self.action_executor.execute_action(action)  # Use the ActionExecutor instance
