# src/core_engine.py

from utils.logger import EventLogger

class CognitiveCore:
    def __init__(self):
        self.logger = EventLogger(enable_drift_tags=True)
        self.state = {}

    def process_input(self, signal):
        self.logger.log(f"Received signal: {signal}", tag="input_received")
        
        decision_output = {
            "signal": signal,
            "processed": True,
            "confidence": signal.get("confidence", 0.0)
        }

        self.logger.log(f"Processed signal: {decision_output}", tag="signal_processed")
        return decision_output

    def reset(self):
        self.logger.log("System state reset", tag="reset")
        self.state = {}
