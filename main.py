"""
-------------------------------------------------
File Name: main
Description:
Author: TianXin
Date：2022-11-29
-------------------------------------------------
"""
import os
import socket
import sys

from PySide6 import QtCore
from PySide6.QtCore import QUrl, Slot, QObject, Signal
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtWebEngineCore import QWebEngineSettings
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import *

from ui.ui_main import Ui_MainWindow


class Window(QMainWindow):
    # 主线程向udp线程传参
    udp_params = QtCore.Signal(list)
    clients = QtCore.Signal(tuple)

    def __init__(self):
        super().__init__()
        self.cur_dir = os.getcwd().replace('\\', '/')
        # UI载入
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # 初始化地图
        self.page = self.ui.webEngineView.page()
        self.init_baidu()
        # UDP参数
        self.pause = False
        # 数据接收主线程
        self.udp = UDP_Thread()
        # 主线程向udp子线程传参
        self.udp_params.connect(self.udp.udp_params_update)
        self.clients.connect(self.udp.add_client)
        self.udp.send_data.connect(self.log_list_view)
        self.udp.send_data.connect(self.send_coord_to_baidu)
        """
        参数
        """
        self.home = []
        """
        控件初始化
        """
        # btn
        self.ui.connect_btn.clicked.connect(self.on_connect_btn_clicked)
        self.ui.over_btn.clicked.connect(self.on_over_btn_clicked)
        self.ui.add_client_btn.clicked.connect(self.on_add_client_btn_clicked)
        # ip and port
        self.ui.ip_text.setText('127.0.0.1')
        self.ui.port_text.setText('9999')
        self.ui.client_ip_text.setText('127.0.0.1')
        self.ui.client_port_text.setText('8888')
        # log list View
        self.coords = []
        self.log_list_model = QtCore.QStringListModel(self.coords)
        self.ui.logList.setModel(self.log_list_model)
        # clients
        self.client_list = []
        self.client_model = QtCore.QStringListModel(self.client_list)
        self.ui.client_listView.setModel(self.client_model)

    def init_baidu(self):
        path = os.getcwd().replace('\\', '/') + "/templates/baidu.html"
        with open(path, encoding="UTF-8") as f:
            data = f.read()
        self.ui.webEngineView.setHtml(data)

    def on_connect_btn_clicked(self):
        print("开始接收数据")
        self.pause = False
        self.update_udp_params()
        self.udp.start()

    def on_over_btn_clicked(self):
        print("终止接收数据")
        self.pause = True
        self.update_udp_params()

    def on_add_client_btn_clicked(self):
        print("添加新终端")
        self.update_client()

    def update_udp_params(self):
        """
        udp参数更新
        :return:
        """
        params = [self.ui.ip_text.toPlainText(), int(self.ui.port_text.toPlainText()), self.pause]
        self.udp_params.emit(params)

    def update_client(self):
        cli = (self.ui.client_ip_text.toPlainText(), int(self.ui.client_port_text.toPlainText()))

        if cli not in self.client_list:
            self.client_list.append('IP:{0},Port:{1}'.format(cli[0], cli[1]))
            self.client_model.setStringList(self.client_list)
            self.ui.client_listView.setModel(self.client_model)
            self.clients.emit(cli)

    def log_list_view(self, addr, coord):
        self.coords.append('addr:{0},coord:{1}'.format(addr, coord))
        self.log_list_model.setStringList(self.coords)
        self.ui.logList.setModel(self.log_list_model)
        self.ui.logList.scrollToBottom()

    def send_coord_to_baidu(self, addr, coord):
        self.page.runJavaScript(f'genCoordsLine(1,' + coord + ')')

    @Slot(str)
    def update_home_point(self, home):
        x, y = home.split(',')
        self.home.append(float(x))
        self.home.append(float(y))


class UDP_Thread(QtCore.QThread):
    send_data = QtCore.Signal(tuple, str)
    recv_data = QtCore.Signal(tuple)

    def __init__(self):
        super().__init__()
        self.ip, self.port, self.pause = None, None, None
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client = []

    def run(self) -> None:
        try:
            self.server.bind((self.ip, self.port))
        except Exception as e:
            print(e)
            pass

        while True:
            data, client_addr = self.server.recvfrom(1024)
            if client_addr in self.client:  # 判断发送数据的是否接收
                # print(client_addr, '%s' % data.decode('utf-8'))
                self.server.sendto(data.upper(), client_addr)
                self.send_data.emit(client_addr, data.decode('utf-8'))
                if self.pause:
                    # self.s.close()
                    break

    def udp_params_update(self, udp_params_list):
        # print(udp_params_list)
        self.ip, self.port, self.pause = udp_params_list

    def add_client(self, client_info):
        if client_info not in self.client:
            # print(client_info)
            self.client.append(client_info)


def win():
    app = QApplication(sys.argv)
    channel = QWebChannel()

    w = Window()
    w.setWindowTitle("USV无人船控制系统")
    channel.registerObject('py', w)
    w.ui.webEngineView.page().setWebChannel(channel)
    w.ui.webEngineView.show()
    w.show()

    # os.environ['QTWEBENGINE_REMOTE_DEBUGGING'] = '9966'
    # dw = QWebEngineView()
    # dw.setWindowTitle('开发人员工具')
    # dw.load(QUrl('http://127.0.0.1:9966'))
    # dw.move(600, 100)
    # dw.show()

    # w.page.load('file:///' + os.getcwd().replace('\\', '/') + "/templates/baidu.html")
    sys.exit(app.exec())


if __name__ == '__main__':
    win()
