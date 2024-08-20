def strategy_b(history_a, history_b):
    if not history_a:
        return False  # No offer to accept yet
    last_offer = history_a[-1]
    # b will lower their acceptance threshold as rounds increase
    threshold = max(20000, 50000 - len(history_b) * 500)  # Dynamic threshold based on rounds
    return last_offer >= threshold  # Accept if the offer meets or exceeds the threshold
