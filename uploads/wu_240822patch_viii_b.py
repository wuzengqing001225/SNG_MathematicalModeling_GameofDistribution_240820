def punishment_tolerance_b_strategy(history_a, history_b):
    if not history_a:
        return False

    last_offer = history_a[-1]
    rejection_count = history_b.count(False)

    # 根据 B 被拒绝的次数，逐渐提高接受门槛
    threshold = 40000 + (rejection_count * 2000)

    return last_offer >= threshold
