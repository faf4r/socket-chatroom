import socket
import sys
import threading
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'generalUi.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def __init__(self, MainWindow, host, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen(10)
        self.chat_room = []
        self.lock = threading.Lock()
        self.setupUi(MainWindow)
        self.start_thread()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(451, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(30, 20, 381, 471))
        self.listWidget.setObjectName("listWidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(332, 517, 91, 41))
        self.pushButton.setObjectName("pushButton")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(40, 516, 271, 41))
        self.lineEdit.setObjectName("lineEdit")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.pushButton.clicked.connect(self.server_chat)
        self.lineEdit.returnPressed.connect(self.server_chat)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "网络聊天室服务端"))
        self.pushButton.setText(_translate("MainWindow", "发送"))

    def start(self):
        while True:
            conn, addr = self.server.accept()
            self.add_connection(conn, addr)

    def start_thread(self):
        thread = threading.Thread(target=self.start)
        thread.daemon = True
        thread.start()

    def add_connection(self, conn, addr):
        user_name = conn.recv(1024).decode()
        self.lock.acquire()
        self.chat_room.append((conn, user_name, addr))
        self.lock.release()
        self.send_others(f"[[{user_name}加入聊天室]]")
        self.listWidget.insertItem(self.listWidget.count(), f"[[{user_name}加入聊天室]]")
        self.listWidget.scrollToBottom()
        thread = threading.Thread(target=self.run, args=(conn, user_name))
        thread.daemon = True
        thread.start()

    def send_others(self, msg):
        self.lock.acquire()
        for user in self.chat_room:
            try:
                user[0].send(msg.encode())
            except Exception as e:
                self.listWidget.insertItem(self.listWidget.count(), str(e))
                self.listWidget.scrollToBottom()
        self.lock.release()

    def run(self, conn, user_name):
        while True:
            try:
                msg = conn.recv(1024).decode()
                self.send_others(f"[{user_name}]> {msg}")
                self.listWidget.insertItem(self.listWidget.count(), f"[{user_name}]> {msg}")
                self.listWidget.scrollToBottom()
            except ConnectionResetError:
                self.del_connection(conn, user_name)
                break

    def del_connection(self, conn, user_name):
        self.lock.acquire()
        for i, user in enumerate(self.chat_room):
            if user[0] == conn:
                del self.chat_room[i]
                self.lock.release()
                self.send_others(f"[[{user_name}离开聊天室]]")
                print(f"[[{user_name}离开聊天室]]")
                break

    def server_chat(self):
        msg = self.lineEdit.text().strip()
        self.send_others(f"$server$>>{msg}")
        self.lineEdit.clear()
        self.listWidget.insertItem(self.listWidget.count(), f"$server$>>{msg}")
        self.listWidget.scrollToBottom()


if __name__ == '__main__':
    host = "localhost"
    port = 8888

    app = QtWidgets.QApplication(sys.argv)
    win = QtWidgets.QMainWindow()
    ui = Ui_MainWindow(win, host, port)
    win.show()
    sys.exit(app.exec_())
