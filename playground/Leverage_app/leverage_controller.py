class LeverageController:
    def __init__(self, model):
        self.model = model

    def update_leverage(self, value):
        self.model.set_leverage(int(value))
        return self.model.get_leverage()
