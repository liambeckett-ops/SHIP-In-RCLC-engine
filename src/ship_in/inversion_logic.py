def invert_signal(signal):
    # Simple placeholder: invert bullish/bearish signals
    return {k: -v if isinstance(v, (int, float)) else v for k, v in signal.items()}
