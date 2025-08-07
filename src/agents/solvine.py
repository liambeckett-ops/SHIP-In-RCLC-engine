class Solvine:
    def __init__(self):
        self.memory_log = []

    def train_from_feedback(self, daily_summary):
        self.memory_log.append(daily_summary)

    def recall_last(self):
        return self.memory_log[-1] if self.memory_log else "No memory yet."
