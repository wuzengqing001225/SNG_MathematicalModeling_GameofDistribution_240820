def cumulative_ladder_b_strategy(history_a, history_b):
    if not history_a:
        return False

    last_offer = history_a[-1]
    rounds_passed = len(history_a)

    # 累积的阶梯增长策略，每次拒绝门槛提高 2000
    threshold = 40000 + rounds_passed * 2000

    return last_offer >= threshold
