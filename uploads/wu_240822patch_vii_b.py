def history_comparison_b_strategy(history_a, history_b):
    if not history_a:
        return False

    last_offer = history_a[-1]
    
    # 每次只接受比前 10 次中的最高报价更高的报价
    if len(history_a) >= 10:
        max_past_offer = max(history_a[-10:])
        return last_offer > max_past_offer
    else:
        return last_offer >= 50000
