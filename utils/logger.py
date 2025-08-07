# utils/logger.py

import datetime

class EventLogger:
    def __init__(self, enable_drift_tags=False):
        self.logs = []
        self.enable_drift = enable_drift_tags

    def log(self, message, tag=None):
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "message": message
        }
        if self.enable_drift and tag:
            entry["drift_tag"] = tag
        self.logs.append(entry)
        print(f"[{entry['timestamp']}] {message}")

    def export(self):
        return self.logs
