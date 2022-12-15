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
    QGridLayout, QGroupBox, QHBoxLayout, QLabel,
    QListView, QMainWindow, QPushButton, QSizePolicy,
    QTabWidget, QTextEdit, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1401, 938)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.layoutWidget4 = QWidget(self.centralwidget)
        self.layoutWidget4.setObjectName(u"layoutWidget4")
        self.layoutWidget4.setGeometry(QRect(0, 10, 1392, 920))
        self.verticalLayout_4 = QVBoxLayout(self.layoutWidget4)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.layoutWidget4)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(361, 31))
        font = QFont()
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_4.addWidget(self.label)

        self.tabWidget = QTabWidget(self.layoutWidget4)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setMinimumSize(QSize(1381, 881))
        self.tab_1 = QWidget()
        self.tab_1.setObjectName(u"tab_1")
        self.layoutWidget1 = QWidget(self.tab_1)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(0, 0, 330, 183))
        self.layout_info = QHBoxLayout(self.layoutWidget1)
        self.layout_info.setObjectName(u"layout_info")
        self.layout_info.setContentsMargins(0, 0, 0, 0)
        self.groupBox_3 = QGroupBox(self.layoutWidget1)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setMinimumSize(QSize(181, 181))
        self.groupBox_3.setMaximumSize(QSize(181, 181))
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.client_listView = QListView(self.groupBox_3)
        self.client_listView.setObjectName(u"client_listView")
        self.client_listView.setMinimumSize(QSize(160, 150))
        self.client_listView.setMaximumSize(QSize(160, 150))
        self.client_listView.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.verticalLayout_5.addWidget(self.client_listView)


        self.layout_info.addWidget(self.groupBox_3)

        self.groupBox_4 = QGroupBox(self.layoutWidget1)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setMinimumSize(QSize(141, 181))
        self.groupBox_4.setMaximumSize(QSize(141, 181))
        self.verticalLayout_6 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.back_home_btn = QPushButton(self.groupBox_4)
        self.back_home_btn.setObjectName(u"back_home_btn")
        self.back_home_btn.setMinimumSize(QSize(75, 24))
        self.back_home_btn.setMaximumSize(QSize(75, 24))

        self.verticalLayout_6.addWidget(self.back_home_btn)


        self.layout_info.addWidget(self.groupBox_4)

        self.layoutWidget2 = QWidget(self.tab_1)
        self.layoutWidget2.setObjectName(u"layoutWidget2")
        self.layoutWidget2.setGeometry(QRect(331, 60, 1031, 779))
        self.verticalLayout = QVBoxLayout(self.layoutWidget2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.webEngineView = QWebEngineView(self.layoutWidget2)
        self.webEngineView.setObjectName(u"webEngineView")
        self.webEngineView.setMinimumSize(QSize(970, 550))
        self.webEngineView.setMaximumSize(QSize(1029, 701))
        self.webEngineView.setUrl(QUrl(u"about:blank"))

        self.verticalLayout.addWidget(self.webEngineView)

        self.logList = QListView(self.layoutWidget2)
        self.logList.setObjectName(u"logList")
        self.logList.setMinimumSize(QSize(961, 70))
        self.logList.setMaximumSize(QSize(1029, 70))

        self.verticalLayout.addWidget(self.logList)

        self.mapType_comboBox = QComboBox(self.tab_1)
        self.mapType_comboBox.setObjectName(u"mapType_comboBox")
        self.mapType_comboBox.setGeometry(QRect(332, 16, 91, 22))
        self.mapType_comboBox.setMinimumSize(QSize(91, 22))
        self.mapType_comboBox.setMaximumSize(QSize(91, 22))
        self.groupBox_2 = QGroupBox(self.tab_1)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(430, 0, 451, 51))
        self.groupBox_2.setMinimumSize(QSize(451, 51))
        self.ip_label = QLabel(self.groupBox_2)
        self.ip_label.setObjectName(u"ip_label")
        self.ip_label.setGeometry(QRect(70, 24, 21, 16))
        self.ip_label.setMinimumSize(QSize(21, 16))
        self.ip_label.setMaximumSize(QSize(21, 16))
        font1 = QFont()
        font1.setPointSize(10)
        self.ip_label.setFont(font1)
        self.client_ip_text = QTextEdit(self.groupBox_2)
        self.client_ip_text.setObjectName(u"client_ip_text")
        self.client_ip_text.setGeometry(QRect(90, 14, 111, 30))
        self.client_ip_text.setMinimumSize(QSize(111, 30))
        self.client_ip_text.setMaximumSize(QSize(111, 30))
        self.port_label = QLabel(self.groupBox_2)
        self.port_label.setObjectName(u"port_label")
        self.port_label.setGeometry(QRect(244, 24, 31, 16))
        self.port_label.setMinimumSize(QSize(31, 16))
        self.port_label.setMaximumSize(QSize(31, 16))
        self.port_label.setFont(font1)
        self.port_label.setFrameShape(QFrame.NoFrame)
        self.client_port_text = QTextEdit(self.groupBox_2)
        self.client_port_text.setObjectName(u"client_port_text")
        self.client_port_text.setGeometry(QRect(280, 15, 81, 30))
        self.client_port_text.setMinimumSize(QSize(81, 30))
        self.client_port_text.setMaximumSize(QSize(81, 30))
        self.add_client_btn = QPushButton(self.groupBox_2)
        self.add_client_btn.setObjectName(u"add_client_btn")
        self.add_client_btn.setGeometry(QRect(370, 15, 75, 31))
        self.add_client_btn.setMinimumSize(QSize(75, 31))
        self.add_client_btn.setMaximumSize(QSize(75, 31))
        self.connect_types_comboBox = QComboBox(self.groupBox_2)
        self.connect_types_comboBox.setObjectName(u"connect_types_comboBox")
        self.connect_types_comboBox.setGeometry(QRect(10, 21, 51, 22))
        self.connect_types_comboBox.setMinimumSize(QSize(51, 22))
        self.connect_types_comboBox.setMaximumSize(QSize(51, 22))
        self.client_serial_port = QComboBox(self.groupBox_2)
        self.client_serial_port.setObjectName(u"client_serial_port")
        self.client_serial_port.setGeometry(QRect(100, 14, 71, 30))
        self.client_serial_port.setMinimumSize(QSize(71, 30))
        self.client_serial_port.setMaximumSize(QSize(71, 30))
        self.client_baud = QComboBox(self.groupBox_2)
        self.client_baud.setObjectName(u"client_baud")
        self.client_baud.setGeometry(QRect(280, 15, 81, 30))
        self.client_baud.setMinimumSize(QSize(81, 30))
        self.client_baud.setMaximumSize(QSize(81, 30))
        self.com_label = QLabel(self.groupBox_2)
        self.com_label.setObjectName(u"com_label")
        self.com_label.setGeometry(QRect(80, 23, 31, 16))
        self.com_label.setMinimumSize(QSize(31, 16))
        self.com_label.setMaximumSize(QSize(31, 16))
        self.baud_label = QLabel(self.groupBox_2)
        self.baud_label.setObjectName(u"baud_label")
        self.baud_label.setGeometry(QRect(202, 24, 41, 16))
        self.baud_label.setMinimumSize(QSize(41, 16))
        self.baud_label.setMaximumSize(QSize(41, 16))
        self.ip_label.raise_()
        self.client_ip_text.raise_()
        self.port_label.raise_()
        self.client_port_text.raise_()
        self.connect_types_comboBox.raise_()
        self.client_serial_port.raise_()
        self.client_baud.raise_()
        self.com_label.raise_()
        self.baud_label.raise_()
        self.add_client_btn.raise_()
        self.groupBox = QGroupBox(self.tab_1)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(900, 0, 441, 51))
        self.groupBox.setMinimumSize(QSize(441, 51))
        self.groupBox.setMaximumSize(QSize(441, 51))
        self.layoutWidget3 = QWidget(self.groupBox)
        self.layoutWidget3.setObjectName(u"layoutWidget3")
        self.layoutWidget3.setGeometry(QRect(10, 15, 428, 33))
        self.horizontalLayout_4 = QHBoxLayout(self.layoutWidget3)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.layoutWidget3)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(21, 16))
        self.label_2.setMaximumSize(QSize(21, 16))
        self.label_2.setFont(font1)
        self.label_2.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_4.addWidget(self.label_2)

        self.ip_text = QTextEdit(self.layoutWidget3)
        self.ip_text.setObjectName(u"ip_text")
        self.ip_text.setMinimumSize(QSize(111, 31))
        self.ip_text.setMaximumSize(QSize(111, 31))

        self.horizontalLayout_4.addWidget(self.ip_text)

        self.label_3 = QLabel(self.layoutWidget3)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(31, 16))
        self.label_3.setMaximumSize(QSize(31, 16))
        self.label_3.setFont(font1)
        self.label_3.setFrameShape(QFrame.NoFrame)

        self.horizontalLayout_4.addWidget(self.label_3)

        self.port_text = QTextEdit(self.layoutWidget3)
        self.port_text.setObjectName(u"port_text")
        self.port_text.setMinimumSize(QSize(71, 31))
        self.port_text.setMaximumSize(QSize(71, 31))

        self.horizontalLayout_4.addWidget(self.port_text)

        self.connect_btn = QPushButton(self.layoutWidget3)
        self.connect_btn.setObjectName(u"connect_btn")
        self.connect_btn.setMinimumSize(QSize(81, 31))
        self.connect_btn.setMaximumSize(QSize(81, 31))

        self.horizontalLayout_4.addWidget(self.connect_btn)

        self.over_btn = QPushButton(self.layoutWidget3)
        self.over_btn.setObjectName(u"over_btn")
        self.over_btn.setMinimumSize(QSize(81, 31))
        self.over_btn.setMaximumSize(QSize(81, 31))

        self.horizontalLayout_4.addWidget(self.over_btn)

        self.tabWidget.addTab(self.tab_1, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.horizontalLayout_2 = QHBoxLayout(self.tab_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.video = QLabel(self.tab_2)
        self.video.setObjectName(u"video")
        self.video.setMinimumSize(QSize(1171, 751))
        self.video.setMaximumSize(QSize(1920, 1080))

        self.horizontalLayout_2.addWidget(self.video)

        self.verticalLayout_2_3 = QVBoxLayout()
        self.verticalLayout_2_3.setObjectName(u"verticalLayout_2_3")
        self.connect_btn_2 = QPushButton(self.tab_2)
        self.connect_btn_2.setObjectName(u"connect_btn_2")
        self.connect_btn_2.setMinimumSize(QSize(187, 24))
        self.connect_btn_2.setMaximumSize(QSize(187, 24))

        self.verticalLayout_2_3.addWidget(self.connect_btn_2)

        self.upload_img_btn = QPushButton(self.tab_2)
        self.upload_img_btn.setObjectName(u"upload_img_btn")

        self.verticalLayout_2_3.addWidget(self.upload_img_btn)

        self.groupBox_2_5 = QGroupBox(self.tab_2)
        self.groupBox_2_5.setObjectName(u"groupBox_2_5")
        self.groupBox_2_5.setMinimumSize(QSize(187, 61))
        self.groupBox_2_5.setMaximumSize(QSize(187, 61))
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_2_5)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_2_3 = QHBoxLayout()
        self.horizontalLayout_2_3.setObjectName(u"horizontalLayout_2_3")
        self.zoom_out_btn = QPushButton(self.groupBox_2_5)
        self.zoom_out_btn.setObjectName(u"zoom_out_btn")
        self.zoom_out_btn.setMinimumSize(QSize(80, 24))
        self.zoom_out_btn.setMaximumSize(QSize(80, 24))

        self.horizontalLayout_2_3.addWidget(self.zoom_out_btn)

        self.zoom_in_btn = QPushButton(self.groupBox_2_5)
        self.zoom_in_btn.setObjectName(u"zoom_in_btn")
        self.zoom_in_btn.setMinimumSize(QSize(79, 24))
        self.zoom_in_btn.setMaximumSize(QSize(79, 24))

        self.horizontalLayout_2_3.addWidget(self.zoom_in_btn)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2_3)


        self.verticalLayout_2_3.addWidget(self.groupBox_2_5)

        self.groupBox_2_6 = QGroupBox(self.tab_2)
        self.groupBox_2_6.setObjectName(u"groupBox_2_6")
        self.groupBox_2_6.setMinimumSize(QSize(187, 121))
        self.groupBox_2_6.setMaximumSize(QSize(187, 121))
        self.gridLayout = QGridLayout(self.groupBox_2_6)
        self.gridLayout.setObjectName(u"gridLayout")
        self.up_left_btn = QPushButton(self.groupBox_2_6)
        self.up_left_btn.setObjectName(u"up_left_btn")
        self.up_left_btn.setMinimumSize(QSize(39, 24))
        self.up_left_btn.setMaximumSize(QSize(39, 24))

        self.gridLayout.addWidget(self.up_left_btn, 0, 0, 1, 1)

        self.top_btn = QPushButton(self.groupBox_2_6)
        self.top_btn.setObjectName(u"top_btn")
        self.top_btn.setMinimumSize(QSize(39, 24))
        self.top_btn.setMaximumSize(QSize(39, 24))

        self.gridLayout.addWidget(self.top_btn, 0, 1, 1, 1)

        self.up_right_btn = QPushButton(self.groupBox_2_6)
        self.up_right_btn.setObjectName(u"up_right_btn")
        self.up_right_btn.setMinimumSize(QSize(39, 24))
        self.up_right_btn.setMaximumSize(QSize(39, 24))

        self.gridLayout.addWidget(self.up_right_btn, 0, 2, 1, 1)

        self.left_btn = QPushButton(self.groupBox_2_6)
        self.left_btn.setObjectName(u"left_btn")
        self.left_btn.setMinimumSize(QSize(39, 24))
        self.left_btn.setMaximumSize(QSize(39, 24))

        self.gridLayout.addWidget(self.left_btn, 1, 0, 1, 1)

        self.pan_auto_btn = QPushButton(self.groupBox_2_6)
        self.pan_auto_btn.setObjectName(u"pan_auto_btn")
        self.pan_auto_btn.setMinimumSize(QSize(39, 24))
        self.pan_auto_btn.setMaximumSize(QSize(39, 24))

        self.gridLayout.addWidget(self.pan_auto_btn, 1, 1, 1, 1)

        self.right_btn = QPushButton(self.groupBox_2_6)
        self.right_btn.setObjectName(u"right_btn")
        self.right_btn.setMinimumSize(QSize(39, 24))
        self.right_btn.setMaximumSize(QSize(39, 24))

        self.gridLayout.addWidget(self.right_btn, 1, 2, 1, 1)

        self.down_left_btn = QPushButton(self.groupBox_2_6)
        self.down_left_btn.setObjectName(u"down_left_btn")
        self.down_left_btn.setMinimumSize(QSize(39, 24))
        self.down_left_btn.setMaximumSize(QSize(39, 24))

        self.gridLayout.addWidget(self.down_left_btn, 2, 0, 1, 1)

        self.bottom_btn = QPushButton(self.groupBox_2_6)
        self.bottom_btn.setObjectName(u"bottom_btn")
        self.bottom_btn.setMinimumSize(QSize(39, 24))
        self.bottom_btn.setMaximumSize(QSize(39, 24))

        self.gridLayout.addWidget(self.bottom_btn, 2, 1, 1, 1)

        self.down_right_btn = QPushButton(self.groupBox_2_6)
        self.down_right_btn.setObjectName(u"down_right_btn")
        self.down_right_btn.setMinimumSize(QSize(39, 24))
        self.down_right_btn.setMaximumSize(QSize(39, 24))

        self.gridLayout.addWidget(self.down_right_btn, 2, 2, 1, 1)


        self.verticalLayout_2_3.addWidget(self.groupBox_2_6)


        self.horizontalLayout_2.addLayout(self.verticalLayout_2_3)

        self.tabWidget.addTab(self.tab_2, "")

        self.verticalLayout_4.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"USV\u65e0\u4eba\u8239\u63a7\u5236\u7cfb\u7edf", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"\u8bbe\u5907\u6811", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"\u8def\u5f84\u89c4\u5212", None))
        self.back_home_btn.setText(QCoreApplication.translate("MainWindow", u"\u81ea\u52a8\u8fd4\u822a", None))
        self.mapType_comboBox.setCurrentText("")
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"\u8fde\u63a5\u7ec8\u7aef", None))
        self.ip_label.setText(QCoreApplication.translate("MainWindow", u"IP", None))
        self.port_label.setText(QCoreApplication.translate("MainWindow", u"Port", None))
        self.add_client_btn.setText(QCoreApplication.translate("MainWindow", u"\u8fde\u63a5\u7ec8\u7aef", None))
        self.com_label.setText(QCoreApplication.translate("MainWindow", u"\u7aef\u53e3", None))
        self.baud_label.setText(QCoreApplication.translate("MainWindow", u"\u6ce2\u7279\u7387", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"\u76d1\u542c\u670d\u52a1\u5668", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"IP", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Port", None))
        self.connect_btn.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb\u63a5\u6536", None))
        self.over_btn.setText(QCoreApplication.translate("MainWindow", u"\u7ed3\u675f\u63a5\u6536", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), QCoreApplication.translate("MainWindow", u"\u822a\u884c\u6570\u636e", None))
        self.video.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.connect_btn_2.setText(QCoreApplication.translate("MainWindow", u"\u8fde\u63a5", None))
        self.upload_img_btn.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.groupBox_2_5.setTitle(QCoreApplication.translate("MainWindow", u"GroupBox", None))
        self.zoom_out_btn.setText("")
        self.zoom_in_btn.setText("")
        self.groupBox_2_6.setTitle(QCoreApplication.translate("MainWindow", u"\u4e91\u53f0", None))
        self.up_left_btn.setText("")
        self.top_btn.setText("")
        self.up_right_btn.setText("")
        self.left_btn.setText("")
        self.pan_auto_btn.setText(QCoreApplication.translate("MainWindow", u"AUTO", None))
        self.right_btn.setText("")
        self.down_left_btn.setText("")
        self.bottom_btn.setText("")
        self.down_right_btn.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"\u76d1\u63a7\u89c6\u9891", None))
    # retranslateUi

