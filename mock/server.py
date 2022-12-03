"""
-------------------------------------------------
File Name: server
Description:
Author: TianXin
Date：2022-12-01
-------------------------------------------------
"""
import socket


def serve():
    # udp传输的服务端无需半连接池，因为通信无需建立双向连接通道，无需三次握手四次挥手，只要知道对方ip和port就行
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(('127.0.0.1', 9998))

    # 通信循环
    while True:
        data, client_addr = server.recvfrom(1024)  # 这里接收用recvfrom
        print(type(client_addr[0]), '%s' % data.decode('utf-8'))
        server.sendto(data.upper(), client_addr)  # 这里发送用sendto


if __name__ == '__main__':
    serve()