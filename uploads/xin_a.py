def _strategy(history_a,history_b):
    import math
    from numpy import random
    if len(history_a)==0:
        return 49999
    else:
        rate = 0
        price = history_a[-1]
       # return price
        i = len(history_a)
        if i>= 1 and i<= 15:
            rate = 0.85 - math.log(i**3 / 0.4, math.e) / 10
        else:
            rate = 0.14514 - (-i) * math.log(i, math.e) / random.randint(40, 50)
        price=price*(1-rate/100)


        return price