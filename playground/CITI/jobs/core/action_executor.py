class ActionExecutor:
    def __init__(self):
        self.actions = []

    def execute_action(self, action_config):
        operation = action_config.find('operation').text
        if operation == 'ProcessData':
            self._process_data(action_config)
        elif operation == 'Backup':
            self._backup(action_config)
        else:
            raise ValueError(f"Unknown action: {operation}")

    def _process_data(self, action_config):
        input_file = action_config.find('./parameters/param[@name="InputFile"]').attrib['value']
        print(f"Processing data from {input_file}")

    def _backup(self, action_config):
        print(f"Executing backup operation")
