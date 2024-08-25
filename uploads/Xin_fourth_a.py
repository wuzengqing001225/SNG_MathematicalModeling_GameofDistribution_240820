def _strategy(history_a,history_b):
    import math
    if not history_a:
        return 50001

    price=history_a[-1]
    i=len(history_a)+1
    rate = (i % 30 + 1) * math.log(i % 30 + 1, math.e)
    if i == 30 or i == 60:
        price = 50001 - i / 30 * 1000
    price = price * (1 - rate / 1500)
    if i == 90:
        price = 50000
    elif i > 90:
        price = price * (1 + rate / 600)
    return price