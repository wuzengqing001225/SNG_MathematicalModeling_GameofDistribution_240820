def accept_over_50000_b(history_a, history_b):
    if not history_a:
        return False
    
    last_offer = history_a[-1]
    if last_offer > 50000:
        return True
    else:
        return False
