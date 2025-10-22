import os
import time

import flask
from flask import Flask, request, jsonify, redirect, Response

import socket
from threading import Thread
import threading

from flask_sslify import SSLify

import data
import sync
from data import load_meta_data
import broadcast_listener
app = Flask(__name__)

@app.route('/api/data/pull', methods=['GET'])
def get_data():
    print("收到拉取数据")
    return jsonify(sync.get_data())

@app.route('/api/data/push', methods=['PUT'])
def put_data():
    print("收到同步数据")
    data = request.get_json()
    print(f"收到数据: {data}")
    res = sync.put_data(data)
    print(f"返回数据: {res}")
    return jsonify(res)

@app.route('/api/toast', methods=['GET'])
def send_toast():
    return jsonify({})

def sync_time_stream():
    while True:
        yield "data: "+sync.get_todo_data().get_sync_time()+"\n\n"
        time.sleep(1)

@app.route('/sync_time', methods=['GET'])
def sync_time():
    return Response(
        sync_time_stream(),
        mimetype="text/event-stream",
        headers={'Cache-Control': 'no-cache'}
    )

if __name__ == '__main__':
    hello_port = data.get_hello_port()
    http_port = data.get_http_port()

    # 监听广播
    broadcast_listener.start_listening(hello_port, http_port)

    # 在后台运行，不显示调试信息
    app.run(host='0.0.0.0', port=http_port, debug=False, threaded=True)
