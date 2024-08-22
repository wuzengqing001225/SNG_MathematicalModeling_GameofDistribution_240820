import math

def optimized_a_strategy(history_a, history_b):
    rounds_passed = len(history_a)
    if rounds_passed < 90:
        return 20000
    else:
        x = rounds_passed - 80
        a = 28580.6
        b = 0.179
        offer = a * math.exp(b * x)
        
        return min(50001, int(offer))
