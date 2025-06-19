class PricingEngine:
    def __init__(self, model):
        self.model = model

    def price(self, option):
        if option.type == 'call':
            return self.model.call_price(option)
        elif option.type == 'put':
            return self.model.put_price(option)
        else:
            raise ValueError("Unknown option type")