# UDP匿名聊天室
"""
广播（发言）之后将暴露自己，服务端会转发自己的消息给其他所有人
client只有在发送信息给server暴露自己后才能收到server转发的消息
同时server挂了之后会发送消息会显示失去连接，接受消息的主线程也会退出，直到server恢复后再次发送消息暴露自己
"""

import sys
import socket
import threading
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def __init__(self, mainwindow: QtWidgets.QApplication, addr: tuple):
        self.addr = addr
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.is_main_running = False
        self.setupUi(mainwindow)

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

        self.pushButton.clicked.connect(self.send)
        self.lineEdit.returnPressed.connect(self.send)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "匿名聊天室客户端"))
        self.pushButton.setText(_translate("MainWindow", "发送"))

    def main_progress(self):
        while True:
            try:
                msg, _ = self.client.recvfrom(1024)
                self.listWidget.insertItem(self.listWidget.count(), msg.decode())
                self.listWidget.scrollToBottom()
            except ConnectionResetError:
                self.listWidget.insertItem(self.listWidget.count(), "【失去连接，请稍后再试...】")
                self.listWidget.scrollToBottom()
                self.is_main_running = False
                break

    def run_main_progress(self):
        thread = threading.Thread(target=self.main_progress)
        thread.daemon = True
        thread.start()

    def send(self):
        msg = self.lineEdit.text()
        if msg == '':
            return
        self.client.sendto(msg.encode(), self.addr)
        self.lineEdit.clear()
        if not self.is_main_running:
            self.run_main_progress()
            self.is_main_running = True


if __name__ == '__main__':
    host = '127.0.0.1'
    port = 80

    app = QtWidgets.QApplication(sys.argv)
    win = QtWidgets.QMainWindow()
    ui = Ui_MainWindow(win, (host, port))
    win.show()
    sys.exit(app.exec_())
