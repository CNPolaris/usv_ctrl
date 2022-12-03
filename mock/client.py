"""
-------------------------------------------------
File Name: clinet
Description:
Author: TianXin
Date：2022-12-02
-------------------------------------------------
"""
import socket
import random
import time
from concurrent.futures import ThreadPoolExecutor


def cli(port, lats, lngs):
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.bind(('127.0.0.1', port))
    x = [119.22901934296017, 119.2292438054453]
    y = [32.07293057976518, 32.07294333935913]
    l = len(lats)
    i = 0
    while True:
        # x_ = random.uniform(x[0], x[1])
        # y_ = random.uniform(y[0], y[1])
        x_ = lats[i]
        y_ = lngs[i]
        # msg = '{' + 'lat:{0}, lng:{1}, alt:0, timestamp:{2}'.format(x_, y_, time.time()) + '}'
        msg = {
            "lng": x_,
            "lat": y_,
            "timestamp": time.time()
        }
        client.sendto(str(msg).encode('utf-8'), ('127.0.0.1', 9999))
        # data, server_addr = client.recvfrom(1024)
        # print(port, data.decode('utf-8'))
        print(port, msg)
        if i == l:
            i = 0
        else:
            i += 1

        time.sleep(1)


def main():
    with open('E:\\just\\海韵湖智能技术实验场\\原始数据\\processed\\baidu_lake.txt') as f:
        lake = f.read()
    lngs = []
    lats = []
    for xy in lake.split(';'):
        y, _, x = xy.partition(',')
        x = float(x.strip())
        y = float(y.strip())
        lats.append(x)
        lngs.append(y)
    pool = ThreadPoolExecutor(max_workers=2)
    c_1 = pool.submit(cli, 8888, lats, lngs)
    c_2 = pool.submit(cli, 6666, lats, lngs)
    pool.shutdown()

if __name__ == '__main__':
    main()
