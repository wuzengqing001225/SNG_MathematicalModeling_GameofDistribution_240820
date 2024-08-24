def _strategy(history_a,history_b):
    import math
    if not history_a:
        return 49999

    price=history_a[-1]
    i=len(history_a)+1
    rate = (i % 30 + 1) * math.log(i % 30 + 1, math.e)
    if i==30 or i==60:
        price=49999

    if i<90:
        price=price*(1-rate / 290)
    elif i == 90:
        price=50000
    else:
        rate=(i)*math.log(i,math.e)/95
        price=price*(1+rate/100)

    return price