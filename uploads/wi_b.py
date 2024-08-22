def default_b_strategy(history_a, history_b):
    if not history_a:
        return False  # No offer to accept yet
    last_offer = history_a[-1]
    return last_offer >= 50000