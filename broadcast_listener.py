from threading import Thread
import socket

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

def start_listening(hello_port: int, http_port: int):
    udp_thread = Thread(target=udp_listener, args=(hello_port, http_port), daemon=True)
    udp_thread.start()