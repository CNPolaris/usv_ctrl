import sys
import time
import os

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QObject, Slot
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QTimer


class Handlers(QObject):

    def __init__(self):
        super().__init__(None)
        self.view = QWebEngineView()
        self.page = self.view.page()
		# 定时发送测试消息的定时器
        self.timer = QTimer()
        self.timer.timeout.connect(self.send_time)
        self.timer.start(100)

    @Slot(str, result=str)
    def hello(self, message):
        """js调用python测试"""
        print('call received')
        return f'hello from python: {message}'

    def send_time(self):
        """python调用js测试"""
        self.page.runJavaScript(f'sysTime("python 本地时间: {time.time()}")')


if __name__ == '__main__':
    app = QApplication(sys.argv)

    channel = QWebChannel()
    handlers = Handlers()
    channel.registerObject('py', handlers)
    handlers.page.setWebChannel(channel)
    url = os.getcwd().replace('\\', '/') + '/templates/index.html'
    handlers.view.load(url)
    handlers.view.show()
    sys.exit(app.exec())

