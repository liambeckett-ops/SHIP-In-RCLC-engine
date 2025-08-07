# src/sentiment_module.py

import random

class SentimentModule:
    def __init__(self):
        self.sentiment_score = 0

    def fetch_data(self):
        # Placeholder for actual API call
        return {"reddit_score": random.uniform(-1, 1)}

    def analyze(self, raw_data):
        # Simple normalization
        score = raw_data.get("reddit_score", 0)
        self.sentiment_score = score
        return {"sentiment": score}
