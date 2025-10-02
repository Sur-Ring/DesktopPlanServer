import os
import time

import flask
from flask import Flask, request, jsonify

import data
import sync

app = Flask(__name__)

@app.route('/api/data/get', methods=['GET'])
def get_data():
    server_data = data.load_todo_data("./data/data.json")
    return jsonify(server_data.to_dict())

@app.route('/api/data/check', methods=['POST'])
def check_data():
    data = request.get_json()
    print(f"Received data: {data}")  # 在实际应用中，这里可以处理数据
    res_dict = sync.sync_data(data)
    return jsonify(res_dict)

@app.route('/api/data/set', methods=['PUT'])
def set_data():
    data = request.get_json()
    print(f"Received data: {data}")  # 在实际应用中，这里可以处理数据
    res_dict = sync.set_data(data)
    return jsonify(res_dict)

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