def time_window_b_strategy(history_a, history_b):
    if not history_a:
        return False

    last_offer = history_a[-1]
    rounds_left = 100 - len(history_a)

    # 在前 50 轮只接受非常高的报价 (> 70000)
    if rounds_left > 50:
        return last_offer >= 70000
    
    # 在 50 到 90 轮之间逐步放松，接受不低于 60000 的报价
    elif rounds_left > 10:
        return last_offer >= 60000
    
    # 在最后 10 轮，接受不低于 50000 的报价
    return last_offer >= 50000
