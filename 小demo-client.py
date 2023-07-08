import datetime
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.bind(('localhost', 8002))
# client.bind(('192.168.51.65', 8002))

# 建立一个连接
client.connect(('192.168.51.86', 8001))
while True:
    s = input()
    client.send(s.encode('utf-8'))
    res = client.recv(1024).decode('utf-8')
    if res == '[!@#$quit]':
        print('[quit]')
        client.close()
        break
    print(f'[server]:{res}')
