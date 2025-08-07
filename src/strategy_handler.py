# src/strategy_handler.py

class StrategyHandler:
    def __init__(self):
        self.current_strategy = None

    def load_strategy(self, name):
        # Load strategy logic (SOXL, inverse ETF, etc)
        self.current_strategy = name

    def execute(self, data):
        if self.current_strategy == "SOXL":
            return self._soxl_strategy(data)
        else:
            return {"decision": "no-op"}

    def _soxl_strategy(self, data):
        # Placeholder for SOXL decision logic
        signal_strength = data.get("confidence", 0)
        return {"decision": "buy" if signal_strength > 0.7 else "wait"}

# src/strategy_handler.py

class StrategyHandler:
    def __init__(self, threshold=0.75):
        self.threshold = threshold

    def execute(self, signal_output):
        confidence = signal_output.get("confidence", 0.0)
        if confidence >= self.threshold:
            return {"decision": "BUY", "rationale": "High confidence"}
        else:
            return {"decision": "HOLD", "rationale": "Uncertain market"}
