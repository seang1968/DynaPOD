class LeverageModel:
    def __init__(self, min_leverage=5, max_leverage=100, step=5):
        self.min_leverage = min_leverage
        self.max_leverage = max_leverage
        self.step = step
        self.leverage = min_leverage

    def set_leverage(self, value):
        value = max(self.min_leverage, min(self.max_leverage, value))
        self.leverage = round(value / self.step) * self.step

    def get_leverage(self):
        return self.leverage
