# src/execution_manager.py

from utils.logger import EventLogger

class ExecutionManager:
    def __init__(self):
        self.logger = EventLogger(enable_drift_tags=True)
        self.trades = []

    def simulate_trade(self, action, price):
        trade = {"action": action, "price": price}
        self.trades.append(trade)
        self.logger.log(f"Simulated trade: {trade}", tag="trade_exec")

    def report(self):
        self.logger.log(f"Trade history report: {self.trades}", tag="report")
        return self.trades

class ExecutionManager:
    def __init__(self):
        self.history = []

    def simulate_trade(self, decision, price=0.00):
        """
        Logs and simulates a trade based on decision
        """
        result = {"action": decision, "price": price}
        self.history.append(result)
        print(f"Simulated trade: {decision.upper()} at ${price}")
        return result

    def report(self):
        return self.history
