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
        with open(file_b_path, 'r') as f:
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
        for b_name, b_strategy in b_strategies:
            player_name = a_name[:-5] if a_name[:-5] == b_name[:-5] else ''
            if 'default' in player_name: player_name = player_name.replace("default", "baseline")

            total_offer = 0
            total_accepted = 0
            total_rounds = 0
            
            # 运行 100 次模拟
            for _ in range(100):
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
                        final_offer = offer
                        break

                total_offer += final_offer
                total_accepted += 1 if accepted else 0
                total_rounds += round_number

            # 计算平均报价和接受率
            average_offer = total_offer / 50
            acceptance_rate = total_accepted / 50

            results.append({
                "player_name": player_name,
                "a_name": a_name,
                "b_name": b_name,
                "average_offer": average_offer,
                "acceptance_rate": acceptance_rate,
                "total_rounds": total_rounds / 50  # 平均回合数
            })

    # 按平均报价排序
    results = sorted(results, key=lambda x: (x['acceptance_rate'] == 0, x['average_offer']))

    return render_template('tournament.html', results=results)

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
