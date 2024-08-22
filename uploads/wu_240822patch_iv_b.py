def probabilistic_b_strategy(history_a, history_b):
    import random
    
    if not history_a:
        return False

    last_offer = history_a[-1]
    acceptance_probability = 0.3 if last_offer < 50000 else 0.7

    return random.random() < acceptance_probability
