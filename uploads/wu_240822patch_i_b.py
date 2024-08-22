def default_b_strategy(history_a, history_b):
    last_offer = history_a[-1] if history_a else None

    if last_offer is None or last_offer < 50000:
        return False
    
    if len(history_b) < 98:
        return last_offer >= 50000
    
    return last_offer >= 50001
