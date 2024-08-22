def ladder_increase_b_strategy(history_a, history_b):
    if not history_a:
        return False

    last_offer = history_a[-1]
    rounds_passed = len(history_a)

    # 每 10 轮门槛增加一次
    threshold = 20000 + (rounds_passed // 10) * 10000
    
    return last_offer >= threshold
