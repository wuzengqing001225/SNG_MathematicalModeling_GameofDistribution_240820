import os
from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import random
import importlib.util
import inspect

app = Flask(__name__)
app.secret_key = 'your_secret_key'
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 默认策略
def default_a_strategy(history_a, history_b):
    return 50000  # A分给B 5万

def default_b_strategy(history_a, history_b):
    return random.choice([True, False])  # B随机接受或拒绝

def find_single_function(module):
    """查找并返回模块中的唯一函数"""
    functions = [func for func in dir(module) if callable(getattr(module, func)) and not func.startswith("__")]
    
    if len(functions) == 1:
        return getattr(module, functions[0])
    else:
        raise ValueError("上传的文件中应仅包含一个函数。")

def load_strategy(file_path, default_strategy):
    try:
        spec = importlib.util.spec_from_file_location("strategy", file_path)
        strategy_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(strategy_module)
        
        # 查找文件中的唯一函数
        strategy = find_single_function(strategy_module)
        
        # 验证函数参数是否符合要求
        if inspect.signature(strategy).parameters.keys() != {'history_a', 'history_b'}:
            print(f"函数的参数不符合要求，使用默认策略。")
            return default_strategy
        
        return strategy
    except Exception as e:
        print(f"加载策略文件时发生错误: {e}")
        return default_strategy

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_a', methods=['POST'])
def upload_a():
    file_a = request.files.get('file_a', None)

    if file_a and file_a.filename != '':
        file_a_path = os.path.join(app.config['UPLOAD_FOLDER'], file_a.filename)
        file_a.save(file_a_path)
        session['a_strategy_path'] = file_a_path  # 存储文件路径到session
        with open(file_a_path, 'r') as f:
            code_a = f.read()
    else:
        session['a_strategy_path'] = None
        code_a = inspect.getsource(default_a_strategy)
    
    return jsonify({"code_a": code_a})

@app.route('/upload_b', methods=['POST'])
def upload_b():
    file_b = request.files.get('file_b', None)

    if file_b and file_b.filename != '':
        file_b_path = os.path.join(app.config['UPLOAD_FOLDER'], file_b.filename)
        file_b.save(file_b_path)
        session['b_strategy_path'] = file_b_path  # 存储文件路径到session
        with open(file_b_path, 'r', encoding="utf-8") as f:
            code_b = f.read()
    else:
        session['b_strategy_path'] = None
        code_b = inspect.getsource(default_b_strategy)
    
    return jsonify({"code_b": code_b})

@app.route('/tournament')
def tournament():
    a_strategies = []
    b_strategies = []

    for filename in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if filename.endswith('_a.py'):
            a_strategies.append((filename, load_strategy(file_path, default_a_strategy)))
        elif filename.endswith('_b.py'):
            b_strategies.append((filename, load_strategy(file_path, default_b_strategy)))

    results = []

    # 进行两两对决，运行 100 次并计算平均结果
    for a_name, a_strategy in a_strategies:
        total_gain = 0
        total_accepted = 0
        total_rounds = 0
        player_name = a_name[:-5]
        if 'default' in player_name: player_name = player_name.replace("default", "baseline")

        # 运行 100 次模拟
        n = 100

        for b_name, b_strategy in b_strategies:
            for _ in range(n):
                history_a = []
                history_b = []
                accepted = False
                final_offer = 0

                for round_number in range(100):
                    offer = a_strategy(history_a, history_b)
                    history_a.append(offer)
                    accept = b_strategy(history_a, history_b)
                    history_b.append(accept)

                    if accept:
                        accepted = True
                        final_offer = offer if offer > 0 else 0
                        break

                total_gain += (100000 - final_offer) if accepted else 0
                total_accepted += 1 if accepted else 0
                total_rounds += round_number

        # 计算平均报价和接受率
        average_gain = total_gain / n / len(b_strategies)
        acceptance_rate = total_accepted / n / len(b_strategies)

        results.append({
            "player_name": player_name,
            "a_name": a_name,
            "average_gain": average_gain,
            "acceptance_rate": acceptance_rate,
            "total_rounds": total_rounds / n / len(b_strategies)  # 平均回合数
        })    

    # 按平均报价排序
    results = sorted(results, key=lambda x: (x['average_gain']), reverse=True)

    return render_template('tournament.html', results=results)

@app.route('/elimination_tournament')
def elimination_tournament():
    a_strategies = []
    b_strategies = []

    # 从上传文件夹中读取所有策略
    for filename in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if filename.endswith('_a.py'):
            a_strategies.append((filename, load_strategy(file_path, default_a_strategy)))
        elif filename.endswith('_b.py'):
            b_strategies.append((filename, load_strategy(file_path, default_b_strategy)))

    a_ranking = []
    b_ranking = []

    # 每回合逐步淘汰一个a和一个b策略
    round_counter = 1
    while len(a_strategies) > 1 and len(b_strategies) > 1:
        a_scores = []
        b_scores = []

        # 计算每个a策略与所有b策略博弈的平均收益
        for a_name, a_strategy in a_strategies:
            total_gain = 0
            for _, b_strategy in b_strategies:
                history_a = []
                history_b = []
                accepted = False
                final_offer = 0

                for _ in range(100):  # 最大回合数为100
                    offer = a_strategy(history_a, history_b)
                    history_a.append(offer)
                    accept = b_strategy(history_a, history_b)
                    history_b.append(accept)

                    if accept:
                        accepted = True
                        final_offer = offer
                        break

                total_gain += final_offer if accepted else 0  # 如果被接受，计入收益

            avg_gain = total_gain / len(b_strategies)
            a_scores.append((a_name, avg_gain))

        # 计算每个b策略与所有a策略博弈的平均收益
        for b_name, b_strategy in b_strategies:
            total_gain = 0
            for _, a_strategy in a_strategies:
                history_a = []
                history_b = []
                accepted = False
                final_offer = 0

                for _ in range(100):  # 最大回合数为100
                    offer = a_strategy(history_a, history_b)
                    history_a.append(offer)
                    accept = b_strategy(history_a, history_b)
                    history_b.append(accept)

                    if accept:
                        accepted = True
                        final_offer = offer
                        break

                total_gain += 100000 - final_offer if accepted else 0  # B的收益是100,000减去A的报价

            avg_gain = total_gain / len(a_strategies)
            b_scores.append((b_name, avg_gain))

        # 找到最低收益的a和b策略
        a_scores.sort(key=lambda x: x[1])
        b_scores.sort(key=lambda x: x[1])

        a_eliminated = a_scores[0]
        b_eliminated = b_scores[0]

        a_strategies = [s for s in a_strategies if s[0] != a_eliminated[0]]
        b_strategies = [s for s in b_strategies if s[0] != b_eliminated[0]]

        a_ranking.append({
            "name": a_eliminated[0],
            "avg_gain": a_eliminated[1],
            "round_eliminated": round_counter
        })
        b_ranking.append({
            "name": b_eliminated[0],
            "avg_gain": b_eliminated[1],
            "round_eliminated": round_counter
        })

        round_counter += 1

    # 将最后剩下的a和b策略设为第一名
    if len(a_strategies) == 1:
        a_ranking.append({
            "name": a_strategies[0][0],
            "avg_gain": 0,  # 最终第一名没有淘汰时的收益
            "round_eliminated": round_counter
        })
    if len(b_strategies) == 1:
        b_ranking.append({
            "name": b_strategies[0][0],
            "avg_gain": 0,  # 最终第一名没有淘汰时的收益
            "round_eliminated": round_counter
        })

    return render_template('elimination_tournament.html', a_ranking=a_ranking, b_ranking=b_ranking)

@app.route('/run_simulation', methods=['POST'])
def run_simulation():
    a_strategy_path = session.get('a_strategy_path', None)
    b_strategy_path = session.get('b_strategy_path', None)

    a_strategy = load_strategy(a_strategy_path, default_a_strategy) if a_strategy_path else default_a_strategy
    b_strategy = load_strategy(b_strategy_path, default_b_strategy) if b_strategy_path else default_b_strategy

    # 模拟运行逻辑
    history_a = []
    history_b = []
    accepted = False
    final_offer = 0
    
    for round_number in range(100):
        offer = a_strategy(history_a, history_b)  # 调用A策略
        history_a.append(offer)
        
        accept = b_strategy(history_a, history_b)  # 调用B策略
        history_b.append(accept)
        
        if accept:
            accepted = True
            final_offer = offer
            break
    
    # 返回模拟结果
    return jsonify({
        "round_number": round_number,
        "final_offer": final_offer,
        "accepted": accepted,
        "history_a": history_a,
        "history_b": history_b
    })

if __name__ == '__main__':
    app.run(debug=True)
