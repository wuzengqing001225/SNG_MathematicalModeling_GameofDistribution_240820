def incremental_acceptance_b(history_a, history_b):
    if not history_a:
        return False
    
    last_offer = history_a[-1]
    rounds_passed = len(history_a)

    # 随着轮次增加逐步接受更低的报价
    threshold = 50000 - (rounds_passed * 500)
    
    return last_offer >= threshold
