def punishment_b(history_a, history_b):
    if not history_a:
        return False

    last_offer = history_a[-1]
    rounds_passed = len(history_a)

    # 在前80轮较为强硬，之后逐步放宽接受门槛
    if rounds_passed < 80:
        return last_offer >= 70000
    elif rounds_passed < 95:
        return last_offer >= 60000
    else:
        return last_offer >= 50000
