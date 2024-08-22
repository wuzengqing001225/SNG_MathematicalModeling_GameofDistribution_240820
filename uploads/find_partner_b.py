def find_partner_b(history_a,history_b):
    if len(history_a)<=28:
        return False
    else:
        for i in range(0,len(history_a)-2):
            if history_a[i]>=history_a[-1]:
                return False
        return True
