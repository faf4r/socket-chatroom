import datetime
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# server.bind(('localhost', 8001))
server.bind(('192.168.51.86', 8001))

server.listen(5)

while True:
    conn, addr = server.accept()
    try:
        # 一次accept就是一个连接，不循环的话就是在等待下一个连接了（可以同时连接几个主机的）
        while True:
            recv = conn.recv(1024).decode('utf-8')
            print(f'[{addr}]:{recv}')
            if recv == 'quit':
                conn.send('[!@#$quit]'.encode('utf-8'))
                conn.close()
                break
            else:
                # conn.send(f"【{datetime.datetime.now()}】 {recv}".encode('utf-8'))
                msg = input()
                conn.send(msg.encode('utf-8'))
                # print(f'[me]:{msg}')
    except Exception as e:
        print(e)
        conn.close()
