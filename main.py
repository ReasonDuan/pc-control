import os
import logging
from flask import Flask, request, redirect, render_template, url_for, flash, session, jsonify
import hashlib
from datetime import datetime

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = os.urandom(24)

SECRET_KEY = "2f4d6982-1235-4b43-816f-c8b125a336de"
users = {'demo': 'demo', 'admin': 'pwd@123456'}
token_set = set()
pc_map = {}

machines = [
    {'name': 'Machine 1', 'status': 'on', 'time': datetime.now()},
    {'name': 'Machine 2', 'status': 'off', 'time': datetime.now()},
    {'name': 'Machine 3', 'status': 'on', 'time': datetime.now()},
]

@app.route('/', methods=['GET'])
def upload_file():
    # 验证令牌是否存在且有效
    if 'token' in session:
        token = session['token']
        if token in token_set:
            return render_template('index.html', machines=machines)
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username] == password:
            # 登录成功，生成令牌并存储到 session 中
            token = md5_encrypt(username)
            token_set.add(token)
            session['token'] = token
            flash('Login successful!', 'success')
            return redirect(url_for('upload_file'))
        else:
            flash('Login failed. Please check your username and password.', 'error')

    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    token = request.headers.get('token')
    if token == SECRET_KEY:
        data = request.get_json()
        logging.info(f'commit data: {data}')
        ip = data.get("ip")
        name = data.get("name")

        # 检查新机器是否已经存在
        machine = next((machine for machine in machines if machine['name'] == name),None)

        if machine:
            # 更新时间
            machine['time'] = datetime.now()
        else:
            machine = {'name': name, 'ip': ip, 'status': 'on', 'time': datetime.now()}
            machines.append(machine)
        return machine

    return "register error.", 500

@app.route('/toggle_status/<int:index>/<string:operation>')
def toggle_status(index, operation):
    # 模拟切换机器状态
    machines[index]['status'] = operation
    return jsonify({'status': machines[index]['status']})

def update_status():
    if 'token' in session:
        token = session['token']
        if token in token_set:

            return render_template('index.html', machines=machines)

    return render_template('login.html')

def md5_encrypt(text):
    # 创建一个 MD5 hash 对象
    md5 = hashlib.md5()
    # 更新 hash 对象的内容，传入要加密的文本（必须是 bytes 类型）
    md5.update(text.encode('utf-8'))
    # 获取加密后的结果
    encrypted_text = md5.hexdigest()

    return encrypted_text

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8006)
