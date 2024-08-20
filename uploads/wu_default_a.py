def strategy_a(history_a, history_b):
    if not history_a:
        return 30000  # Start with a lower offer
    if history_b[-1]:
        return history_a[-1]  # Keep the same offer if b accepted the previous one
    if len(history_a) < 50:  # In the early rounds, increase offers gradually
        return history_a[-1] + 2000
    else:  # In later rounds, start making bigger jumps
        return history_a[-1] + 5000