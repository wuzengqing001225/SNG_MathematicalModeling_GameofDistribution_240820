# 优化后的策略函数
def optimized_a_strategy(history_a, history_b):
    import math
    import numpy as np
    from scipy.optimize import curve_fit

    # 定义指数函数
    def exp_func(x, a, b):
        return a * np.exp(b * x)
    
    rounds_passed = len(history_a)

    # 如果游戏还在前 90 回合，保持低报价
    if rounds_passed < 90:
        return 20000

    # 如果回合在 90 轮或之后，计算报价
    else:
        # 给定的两个数据点 (90轮时 20000，100轮时 50001)
        x_data = np.array([0, 10])
        y_data = np.array([20000, 50001])

        # 使用curve_fit拟合a和b
        # popt, _ = curve_fit(exp_func, x_data, y_data)
        # a, b = popt
        # print(popt)
        a, b = [3.88768898e+03, 2.55422812e-01]

        # 计算当前回合的报价
        x = rounds_passed - 90  # x 从第 90 轮开始计数
        offer = a * math.exp(b * x) + 15000
        
        # 确保报价不超过 50001
        return min(50001, int(offer))
