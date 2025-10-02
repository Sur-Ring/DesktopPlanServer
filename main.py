import os
import time

import flask
from flask import Flask, request, jsonify

from data import *

app = Flask(__name__)
todo_data = load_todo_data("./data/data.json")
config_data = load_config("./data/cfg.json")

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify(todo_data.to_dict())

@app.route('/api/data', methods=['POST'])
def sync_data():
    # 尝试更新服务器数据
    # 如果客户端是最新数据, 那么通知客户端
    # 如果客户端是旧数据, 返回服务器数据
    # 如果两侧失去同步, 那么返回客户端数据
    sync_stat = -1 # 负数. 为错误保留; 0. 无需同步; 1. 更新到服务器; 2. 拉取服务器数据; 3. 失去同步
    data = request.get_json()
    print(f"Received data: {data}")  # 在实际应用中，这里可以处理数据
    return jsonify({"sync_stat": sync_stat, "data": data})

# @app.route('/api/shutdown', methods=['POST'])
# def shutdown():
#     """安全关闭服务器的API端点"""
#
#     def shutdown_server():
#         time.sleep(1)
#         os._exit(0)
#
#     threading.Thread(target=shutdown_server).start()
#     return jsonify({"message": "Server is shutting down"})

if __name__ == '__main__':
    # 在后台运行，不显示调试信息
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)