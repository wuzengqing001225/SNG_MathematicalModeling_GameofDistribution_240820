# 数学建模分配的博弈问题

![image](https://github.com/wuzengqing001225/SNG_MathematicalModeling_GameofDistribution_240820/blob/main/static/images/cover.png)

## 任务描述

本项目是一个博弈模拟器，允许用户上传自定义的策略文件，以模拟两个玩家（A 和 B）在有限轮次内如何分配两人在金蝶游乐场游玩中捡到的10万金蝶币。

如果双方达成协议，游戏结束，小伙伴都能玩得愉快。如果不能达成协议，双方都无法获得任何金钱，而是直接上缴。

每一次协商，B如果不接受，A可以重新报价，最多重复100次流程。A每次选择报价，B选择是否接受（`True`接受，`False`不接受）。

最终大家的策略混合运行，看谁得分最高。

## 功能

- 上传策略：学生可以上传自定义的策略代码文件来控制 A 和 B 的行为。
- 模拟运行：系统运行模拟，通过 A 和 B 的策略计算在每轮的报价和是否接受，并最终显示模拟结果。
- 策略代码的格式要求
  - 每个策略文件应该**定义且只定义**一个函数
  - A 的策略函数：接受两个参数 `history_a` 和 `history_b`，并返回 A 的下一个报价金额（范围为 `0` 到 `100,000`）。

    ```Python
    # A 的默认策略：A 初始报价为 50000，之后的报价不变。
    def a_strategy(history_a, history_b):
      # 计算 A 的下一个报价金额
      return 50000  # 返回的金额在 0 到 100,000 之间
    ```
  - B 的策略函数：接受两个参数 `history_a` 和 `history_b`，并返回布尔值 `True` 或 `False`，表示 B 是否接受 A 的当前报价。

    ```Python
    # B 的默认策略：B 以随机方式决定是否接受 A 的报价。
    def b_strategy(history_a, history_b):
      # 计算 B 是否接受 A 的当前报价
      import random
      return random.choice([True, False])  # 随机返回 True 或 False
    ```
  - 如果没有上传自定义策略，系统会使用默认策略
  - 任何未遵循上述输入输出规则的代码将会导致使用系统默认策略。
  - `import`请放置在函数内部

## 运行依赖项

```
Flask==3.0.3
```

## 运行方法

1. `python app.py`
2. 打开 http://127.0.0.1:5000

## 项目信息

```
中福会少年宫2024暑期数学建模班 24/08/20
```
