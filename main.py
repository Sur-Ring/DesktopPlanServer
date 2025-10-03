import os
import time

import flask
from flask import Flask, request, jsonify

import socket
from threading import Thread
import socket
import threading

import data
import sync
from data import load_meta_data

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

def udp_listener(hello_port: int, http_port: int):
    # 创建UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # 绑定到所有接口的5001端口
    sock.bind(('', hello_port))

    while True:
        data, addr = sock.recvfrom(1024)
        if data.decode() == "DISCOVER_FLASK_SERVICE":
            # 发送回复，包括自己的IP和服务端口
            # 注意：这里我们获取自己的IP地址，但注意可能有多个IP，需要选择正确的那个
            # 这里我们简单回复一个固定的消息，包含自己的IP（addr是发送者的IP，我们不需要，我们需要自己的IP）
            # 获取自己的IP地址（与外部通信的IP）可能比较复杂，这里我们可以用addr[0]来获取发送者的IP，然后通过这个接口回复，但是这样不一定正确。
            # 另一种方法是获取本机所有IP，然后选择一个非回环的IPv4地址，但这样可能多个，我们可以选择与发送者在同一子网的IP。
            # 简单起见，我们可以回复一个字符串，比如"FLASK_SERVICE_IP:5000"，然后客户端解析。
            # 但是，我们如何知道自己的IP呢？我们可以通过socket.gethostbyname(socket.gethostname())获取，但可能不准确。
            # 这里我们使用一个简单的方法：通过创建一个到发送者的连接来获取自己的IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect((addr[0], 1))
            my_ip = s.getsockname()[0]
            s.close()
            reply = f"FLASK_SERVICE:{my_ip}:{http_port}"
            # reply = f"FLASK_SERVICE_PORT:{http_port}"
            sock.sendto(reply.encode(), addr)
            print(f"Replied to {addr} with {reply}")

if __name__ == '__main__':
    meta_data = data.load_meta_data("./data/meta.json")
    udp_thread = Thread(target=udp_listener, args=(meta_data.hello_port, meta_data.http_port), daemon=True)
    udp_thread.start()

    # 在后台运行，不显示调试信息
    app.run(host='0.0.0.0', port=meta_data.http_port, debug=False, threaded=True)