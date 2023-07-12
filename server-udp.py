# 匿名聊天室
"""
server将所有接受到信息的address添加到集合中，并将接受到的所有信息转发给集合中的地址
"""
import sys
import socket
import threading
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def __init__(self, mainwindow: QtWidgets.QMainWindow, address: tuple):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind(address)
        self.setupUi(mainwindow)
        self.addresses = set()
        self.run_main_process()

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

        self.pushButton.clicked.connect(self.server_send)
        self.lineEdit.returnPressed.connect(self.server_send)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "匿名聊天室服务端"))
        self.pushButton.setText(_translate("MainWindow", "发送"))

    def send(self, msg):
        for addr in self.addresses:
            self.server.sendto(msg.encode(), addr)

    def main_process(self):
        while True:
            try:
                msg, addr = self.server.recvfrom(1024)
                self.addresses.add(addr)
                msg = msg.decode()
                self.send(msg)
                self.listWidget.insertItem(self.listWidget.count(), msg)
                self.listWidget.scrollToBottom()
            except ConnectionResetError:
                pass

    def run_main_process(self):
        thread = threading.Thread(target=self.main_process)
        thread.daemon = True
        thread.start()

    def server_send(self):
        msg = '[[server]]>>' + self.lineEdit.text()
        if self.lineEdit.text().strip() == '':
            return
        threading.Thread(target=self.send, args=(msg,)).start()
        self.listWidget.insertItem(self.listWidget.count(), msg)
        self.listWidget.scrollToBottom()
        self.lineEdit.clear()


if __name__ == '__main__':
    host = '0.0.0.0'
    port = 80

    app = QtWidgets.QApplication(sys.argv)
    win = QtWidgets.QMainWindow()
    ui = Ui_MainWindow(win, (host, port))
    win.show()
    sys.exit(app.exec_())
