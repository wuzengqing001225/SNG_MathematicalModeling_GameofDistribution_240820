def unsound_mind_lower_50000_a(history_a, history_b):
    import random
    if not history_a:
        return random.randint(0, 100000)
    else:
        last_offer = history_a[-1]
        return max(last_offer - 1, 0)
