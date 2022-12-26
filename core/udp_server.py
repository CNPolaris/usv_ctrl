"""
-------------------------------------------------
File Name: udp_server
Description: 该模块是实现接收udp传输的坐标数据的线程
Author: TianXin
Date：2022-12-26
-------------------------------------------------
"""
import socket
from PySide6 import QtCore


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
