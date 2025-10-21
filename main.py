import os
import time

import flask
from flask import Flask, request, jsonify

import socket
from threading import Thread
import threading

import data
import sync
from data import load_meta_data
import broadcast_listener

app = Flask(__name__)

@app.route('/api/data/pull', methods=['GET'])
def pull_data():
    return jsonify(sync.pull_data())

@app.route('/api/data/push', methods=['PUT'])
def push_data():
    data = request.get_json()
    print(f"Received push data: {data}")  # 在实际应用中，这里可以处理数据
    return jsonify(sync.push_data(data))

@app.route('/api/toast', methods=['GET'])
def send_toast():
    return jsonify({})

if __name__ == '__main__':
    hello_port = data.get_hello_port()
    http_port = data.get_http_port()

    # 监听广播
    broadcast_listener.start_listening(hello_port, http_port)

    # 在后台运行，不显示调试信息
    app.run(host='0.0.0.0', port=http_port, debug=False, threaded=True)