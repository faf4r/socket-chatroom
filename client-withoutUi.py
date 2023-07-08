import socket
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = 'localhost'
port = 8888

client.connect((host, port))

user_name = client.getsockname()
def init():
    global user_name
    user_name = input("请输入昵称：").strip()
    client.send(user_name.encode())

def receive():
    while True:
        msg = client.recv(1024).decode()
        print(msg)

def send():
    while True:
        msg = input(f'[{user_name}]#')
        client.send(msg.encode())


init()
thread = threading.Thread(target=receive)
thread.daemon = True
thread.start()
send()
