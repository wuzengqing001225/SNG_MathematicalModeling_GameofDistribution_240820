def default_a_strategy(history_a, history_b):
    if len(history_a) == 0:
        return 20000
    if len(history_a) == 1:
        return 42000
    if len(history_a) == 2:
        return 50000
    if len(history_a) == 29:
        return 50001
    if len(history_a) <= 94:
        return 0
    if len(history_a) <= 95:
        return 1
    if len(history_a) <= 96:
        return 20000
    if len(history_a) <= 97:
        return 50000
    if len(history_a) <= 98:
        return 50001
    return 1000