import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 8888))

server.listen(1)

chat_room = []

def run(conn, user_name):
    while True:
        try:
            msg = conn.recv(1024).decode()
            send_others(conn, user_name, f"[{user_name}]> {msg}")
            print(f"[{user_name}]> {msg}")
        except ConnectionResetError:
            del_connection(conn, user_name)
            break

def send_others(conn, user_name, msg):
    for user in chat_room:
        # 发送给本人？不发就注释掉，客户端GUI看得见自己发言，服务端则不用GUI
        # if user[0] == conn:
        #     continue
        user[0].send(msg.encode())

def add_connection(conn, addr):
    user_name = conn.recv(1024).decode()
    chat_room.append((conn, user_name, addr))
    send_others(conn, user_name, f"[[{user_name}加入聊天室]]")
    print(f"[[{user_name}加入聊天室]]")
    thread = threading.Thread(target=run, args=(conn, user_name))
    thread.daemon = True
    thread.start()

def del_connection(conn, user_name):
    for i, user in enumerate(chat_room):
        if user[0] == conn:
            del chat_room[i]
            send_others(conn, user_name, f"[[{user_name}离开聊天室]]")
            print(f"[[{user_name}离开聊天室]]")
            break

# server可发言
def server_chat():
    while True:
        try:
            msg = input("$server$>>")
            send_others(None, "$server$", f"[server]>> {msg}")
        except Exception as e:
            print(e)


thread = threading.Thread(target=server_chat)
thread.daemon = True
thread.start()

while True:
    conn, addr = server.accept()
    add_connection(conn, addr)
