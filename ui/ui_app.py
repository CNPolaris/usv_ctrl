# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'app.ui'
##
## Created by: Qt User Interface Compiler version 6.4.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QComboBox, QFrame,
    QGroupBox, QLabel, QListView, QMainWindow,
    QPushButton, QSizePolicy, QTextEdit, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1235, 903)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.webEngineView = QWebEngineView(self.centralwidget)
        self.webEngineView.setObjectName(u"webEngineView")
        self.webEngineView.setGeometry(QRect(340, 121, 891, 681))
        self.webEngineView.setUrl(QUrl(u"about:blank"))
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(420, 10, 361, 31))
        font = QFont()
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)
        self.logList = QListView(self.centralwidget)
        self.logList.setObjectName(u"logList")
        self.logList.setGeometry(QRect(340, 800, 891, 101))
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(780, 60, 441, 51))
        self.ip_text = QTextEdit(self.groupBox)
        self.ip_text.setObjectName(u"ip_text")
        self.ip_text.setGeometry(QRect(30, 14, 111, 31))
        self.port_text = QTextEdit(self.groupBox)
        self.port_text.setObjectName(u"port_text")
        self.port_text.setGeometry(QRect(180, 14, 71, 31))
        self.connect_btn = QPushButton(self.groupBox)
        self.connect_btn.setObjectName(u"connect_btn")
        self.connect_btn.setGeometry(QRect(260, 14, 81, 31))
        self.over_btn = QPushButton(self.groupBox)
        self.over_btn.setObjectName(u"over_btn")
        self.over_btn.setGeometry(QRect(350, 14, 81, 31))
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 20, 21, 16))
        font1 = QFont()
        font1.setPointSize(10)
        self.label_2.setFont(font1)
        self.label_2.setAlignment(Qt.AlignCenter)
        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(150, 20, 31, 16))
        self.label_3.setFont(font1)
        self.label_3.setFrameShape(QFrame.NoFrame)
        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(340, 60, 411, 51))
        self.ip_label = QLabel(self.groupBox_2)
        self.ip_label.setObjectName(u"ip_label")
        self.ip_label.setGeometry(QRect(70, 20, 21, 16))
        self.ip_label.setFont(font1)
        self.client_ip_text = QTextEdit(self.groupBox_2)
        self.client_ip_text.setObjectName(u"client_ip_text")
        self.client_ip_text.setGeometry(QRect(90, 14, 111, 30))
        self.port_label = QLabel(self.groupBox_2)
        self.port_label.setObjectName(u"port_label")
        self.port_label.setGeometry(QRect(210, 20, 31, 16))
        self.port_label.setFont(font1)
        self.port_label.setFrameShape(QFrame.NoFrame)
        self.client_port_text = QTextEdit(self.groupBox_2)
        self.client_port_text.setObjectName(u"client_port_text")
        self.client_port_text.setGeometry(QRect(240, 14, 81, 30))
        self.add_client_btn = QPushButton(self.groupBox_2)
        self.add_client_btn.setObjectName(u"add_client_btn")
        self.add_client_btn.setGeometry(QRect(330, 14, 75, 31))
        self.connect_types_comboBox = QComboBox(self.groupBox_2)
        self.connect_types_comboBox.setObjectName(u"connect_types_comboBox")
        self.connect_types_comboBox.setGeometry(QRect(10, 19, 51, 22))
        self.client_serial_port = QComboBox(self.groupBox_2)
        self.client_serial_port.setObjectName(u"client_serial_port")
        self.client_serial_port.setGeometry(QRect(100, 13, 71, 30))
        self.client_baud = QComboBox(self.groupBox_2)
        self.client_baud.setObjectName(u"client_baud")
        self.client_baud.setGeometry(QRect(230, 13, 81, 30))
        self.com_label = QLabel(self.groupBox_2)
        self.com_label.setObjectName(u"com_label")
        self.com_label.setGeometry(QRect(70, 20, 31, 16))
        self.baud_label = QLabel(self.groupBox_2)
        self.baud_label.setObjectName(u"baud_label")
        self.baud_label.setGeometry(QRect(180, 20, 41, 16))
        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setGeometry(QRect(0, 120, 181, 181))
        self.client_listView = QListView(self.groupBox_3)
        self.client_listView.setObjectName(u"client_listView")
        self.client_listView.setGeometry(QRect(10, 22, 160, 150))
        self.client_listView.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.groupBox_4 = QGroupBox(self.centralwidget)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setGeometry(QRect(180, 120, 141, 231))
        self.back_home_btn = QPushButton(self.groupBox_4)
        self.back_home_btn.setObjectName(u"back_home_btn")
        self.back_home_btn.setGeometry(QRect(10, 20, 75, 24))
        self.mapType_comboBox = QComboBox(self.centralwidget)
        self.mapType_comboBox.setObjectName(u"mapType_comboBox")
        self.mapType_comboBox.setGeometry(QRect(240, 80, 91, 22))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"USV\u65e0\u4eba\u8239\u63a7\u5236\u7cfb\u7edf", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u76d1\u542c\u670d\u52a1\u5668", None))
        self.connect_btn.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb\u63a5\u6536", None))
        self.over_btn.setText(QCoreApplication.translate("MainWindow", u"\u7ed3\u675f\u63a5\u6536", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"IP", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Port", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"\u8fde\u63a5\u7ec8\u7aef", None))
        self.ip_label.setText(QCoreApplication.translate("MainWindow", u"IP", None))
        self.port_label.setText(QCoreApplication.translate("MainWindow", u"Port", None))
        self.add_client_btn.setText(QCoreApplication.translate("MainWindow", u"\u8fde\u63a5\u7ec8\u7aef", None))
        self.com_label.setText(QCoreApplication.translate("MainWindow", u"\u7aef\u53e3", None))
        self.baud_label.setText(QCoreApplication.translate("MainWindow", u"\u6ce2\u7279\u7387", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"\u8bbe\u5907\u6811", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"\u8def\u5f84\u89c4\u5212", None))
        self.back_home_btn.setText(QCoreApplication.translate("MainWindow", u"\u81ea\u52a8\u8fd4\u822a", None))
        self.mapType_comboBox.setCurrentText("")
    # retranslateUi

