def default_a_strategy(history_a, history_b):
    if len(history_a) <= 95:
        return 0
    if len(history_a) <= 96:
        return 1
    if len(history_a) <= 97:
        return 20000
    if len(history_a) <= 98:
        return 50000
    return 50001