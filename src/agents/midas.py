class Midas:
    def __init__(self, budget_percent=0.3):
        self.budget_percent = budget_percent
        self.history = []
    
    def evaluate_trade(self, signal_data):
        # Placeholder logic
        decision = "buy" if signal_data.get("momentum") > 0.5 else "hold"
        self.history.append((signal_data, decision))
        return decision

    def report(self):
        return {"history": self.history[-5:]}  # show last 5 trades
