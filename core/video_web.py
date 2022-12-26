"""
-------------------------------------------------
File Name: video
Description: 用于将监控视频推送到云端的线程
Author: TianXin
Date：2022-12-26
-------------------------------------------------
"""
import websocket
from PySide6 import QtCore
from websocket import ABNF


class VideoWebThread(QtCore.QThread):
    def __init__(self):
        super().__init__()
        self.url = 'ws://127.0.0.1:8000/ship/video/1/'
        self.data = "test upload"
        self.ws = websocket.WebSocket()

    def run(self) -> None:
        print("VideoUpload")
        self.ws.connect(self.url)

    def recv_img(self, data):
        self.ws.send(data, opcode=ABNF.OPCODE_BINARY)
