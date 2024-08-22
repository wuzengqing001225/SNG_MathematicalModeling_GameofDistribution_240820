def find_partner_b(history_a,history_b):
    if len(history_a) <= 28:
        return False
    else:
        return max(history_a[:-2]) < history_a[-1]
