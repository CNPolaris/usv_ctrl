# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_hk.ui'
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
from PySide6.QtWidgets import (QApplication, QGroupBox, QLabel, QMainWindow,
    QPushButton, QSizePolicy, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(959, 767)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(20, 60, 711, 621))
        self.video = QLabel(self.groupBox)
        self.video.setObjectName(u"video")
        self.video.setGeometry(QRect(50, 40, 641, 561))
        self.connect_btn = QPushButton(self.centralwidget)
        self.connect_btn.setObjectName(u"connect_btn")
        self.connect_btn.setGeometry(QRect(770, 70, 75, 24))
        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(730, 170, 191, 141))
        self.top_btn = QPushButton(self.groupBox_2)
        self.top_btn.setObjectName(u"top_btn")
        self.top_btn.setGeometry(QRect(80, 40, 41, 24))
        self.bottom_btn = QPushButton(self.groupBox_2)
        self.bottom_btn.setObjectName(u"bottom_btn")
        self.bottom_btn.setGeometry(QRect(80, 100, 41, 24))
        self.left_btn = QPushButton(self.groupBox_2)
        self.left_btn.setObjectName(u"left_btn")
        self.left_btn.setGeometry(QRect(30, 70, 41, 24))
        self.right_btn = QPushButton(self.groupBox_2)
        self.right_btn.setObjectName(u"right_btn")
        self.right_btn.setGeometry(QRect(130, 70, 41, 24))
        self.pan_auto_btn = QPushButton(self.groupBox_2)
        self.pan_auto_btn.setObjectName(u"pan_auto_btn")
        self.pan_auto_btn.setGeometry(QRect(80, 70, 41, 24))
        self.up_left_btn = QPushButton(self.groupBox_2)
        self.up_left_btn.setObjectName(u"up_left_btn")
        self.up_left_btn.setGeometry(QRect(30, 40, 41, 24))
        self.up_right_btn = QPushButton(self.groupBox_2)
        self.up_right_btn.setObjectName(u"up_right_btn")
        self.up_right_btn.setGeometry(QRect(130, 40, 41, 24))
        self.down_left_btn = QPushButton(self.groupBox_2)
        self.down_left_btn.setObjectName(u"down_left_btn")
        self.down_left_btn.setGeometry(QRect(30, 100, 41, 24))
        self.down_right_btn = QPushButton(self.groupBox_2)
        self.down_right_btn.setObjectName(u"down_right_btn")
        self.down_right_btn.setGeometry(QRect(130, 100, 41, 24))
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"GroupBox", None))
        self.video.setText("")
        self.connect_btn.setText(QCoreApplication.translate("MainWindow", u"\u8fde\u63a5", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"\u4e91\u53f0", None))
        self.top_btn.setText("")
        self.bottom_btn.setText("")
        self.left_btn.setText("")
        self.right_btn.setText("")
        self.pan_auto_btn.setText(QCoreApplication.translate("MainWindow", u"AUTO", None))
        self.up_left_btn.setText("")
        self.up_right_btn.setText("")
        self.down_left_btn.setText("")
        self.down_right_btn.setText("")
    # retranslateUi

