def run_loop(agent, signal_stream):
    results = []
    for signal in signal_stream:
        decision = agent.evaluate_trade(signal)
        results.append(decision)
    return results
