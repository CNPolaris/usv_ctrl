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
from PySide6.QtWidgets import (QApplication, QGridLayout, QGroupBox, QHBoxLayout,
    QLabel, QMainWindow, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1316, 849)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.video = QLabel(self.centralwidget)
        self.video.setObjectName(u"video")
        self.video.setMinimumSize(QSize(960, 640))
        self.video.setMaximumSize(QSize(1920, 1080))

        self.horizontalLayout_2.addWidget(self.video)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.connect_btn = QPushButton(self.centralwidget)
        self.connect_btn.setObjectName(u"connect_btn")
        self.connect_btn.setMinimumSize(QSize(187, 24))
        self.connect_btn.setMaximumSize(QSize(187, 24))

        self.verticalLayout_3.addWidget(self.connect_btn)

        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setMinimumSize(QSize(187, 61))
        self.groupBox_3.setMaximumSize(QSize(187, 61))
        self.verticalLayout = QVBoxLayout(self.groupBox_3)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.zoom_out_btn = QPushButton(self.groupBox_3)
        self.zoom_out_btn.setObjectName(u"zoom_out_btn")
        self.zoom_out_btn.setMinimumSize(QSize(80, 24))
        self.zoom_out_btn.setMaximumSize(QSize(80, 24))

        self.horizontalLayout.addWidget(self.zoom_out_btn)

        self.zoom_in_btn = QPushButton(self.groupBox_3)
        self.zoom_in_btn.setObjectName(u"zoom_in_btn")
        self.zoom_in_btn.setMinimumSize(QSize(79, 24))
        self.zoom_in_btn.setMaximumSize(QSize(79, 24))

        self.horizontalLayout.addWidget(self.zoom_in_btn)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.verticalLayout_3.addWidget(self.groupBox_3)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setMinimumSize(QSize(187, 121))
        self.groupBox_2.setMaximumSize(QSize(187, 121))
        self.gridLayout = QGridLayout(self.groupBox_2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.up_left_btn = QPushButton(self.groupBox_2)
        self.up_left_btn.setObjectName(u"up_left_btn")
        self.up_left_btn.setMinimumSize(QSize(39, 24))
        self.up_left_btn.setMaximumSize(QSize(39, 24))

        self.gridLayout.addWidget(self.up_left_btn, 0, 0, 1, 1)

        self.top_btn = QPushButton(self.groupBox_2)
        self.top_btn.setObjectName(u"top_btn")
        self.top_btn.setMinimumSize(QSize(39, 24))
        self.top_btn.setMaximumSize(QSize(39, 24))

        self.gridLayout.addWidget(self.top_btn, 0, 1, 1, 1)

        self.up_right_btn = QPushButton(self.groupBox_2)
        self.up_right_btn.setObjectName(u"up_right_btn")
        self.up_right_btn.setMinimumSize(QSize(39, 24))
        self.up_right_btn.setMaximumSize(QSize(39, 24))

        self.gridLayout.addWidget(self.up_right_btn, 0, 2, 1, 1)

        self.left_btn = QPushButton(self.groupBox_2)
        self.left_btn.setObjectName(u"left_btn")
        self.left_btn.setMinimumSize(QSize(39, 24))
        self.left_btn.setMaximumSize(QSize(39, 24))

        self.gridLayout.addWidget(self.left_btn, 1, 0, 1, 1)

        self.pan_auto_btn = QPushButton(self.groupBox_2)
        self.pan_auto_btn.setObjectName(u"pan_auto_btn")
        self.pan_auto_btn.setMinimumSize(QSize(39, 24))
        self.pan_auto_btn.setMaximumSize(QSize(39, 24))

        self.gridLayout.addWidget(self.pan_auto_btn, 1, 1, 1, 1)

        self.right_btn = QPushButton(self.groupBox_2)
        self.right_btn.setObjectName(u"right_btn")
        self.right_btn.setMinimumSize(QSize(39, 24))
        self.right_btn.setMaximumSize(QSize(39, 24))

        self.gridLayout.addWidget(self.right_btn, 1, 2, 1, 1)

        self.down_left_btn = QPushButton(self.groupBox_2)
        self.down_left_btn.setObjectName(u"down_left_btn")
        self.down_left_btn.setMinimumSize(QSize(39, 24))
        self.down_left_btn.setMaximumSize(QSize(39, 24))

        self.gridLayout.addWidget(self.down_left_btn, 2, 0, 1, 1)

        self.bottom_btn = QPushButton(self.groupBox_2)
        self.bottom_btn.setObjectName(u"bottom_btn")
        self.bottom_btn.setMinimumSize(QSize(39, 24))
        self.bottom_btn.setMaximumSize(QSize(39, 24))

        self.gridLayout.addWidget(self.bottom_btn, 2, 1, 1, 1)

        self.down_right_btn = QPushButton(self.groupBox_2)
        self.down_right_btn.setObjectName(u"down_right_btn")
        self.down_right_btn.setMinimumSize(QSize(39, 24))
        self.down_right_btn.setMaximumSize(QSize(39, 24))

        self.gridLayout.addWidget(self.down_right_btn, 2, 2, 1, 1)


        self.verticalLayout_3.addWidget(self.groupBox_2)


        self.horizontalLayout_2.addLayout(self.verticalLayout_3)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.video.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.connect_btn.setText(QCoreApplication.translate("MainWindow", u"\u8fde\u63a5", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"GroupBox", None))
        self.zoom_out_btn.setText("")
        self.zoom_in_btn.setText("")
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"\u4e91\u53f0", None))
        self.up_left_btn.setText("")
        self.top_btn.setText("")
        self.up_right_btn.setText("")
        self.left_btn.setText("")
        self.pan_auto_btn.setText(QCoreApplication.translate("MainWindow", u"AUTO", None))
        self.right_btn.setText("")
        self.down_left_btn.setText("")
        self.bottom_btn.setText("")
        self.down_right_btn.setText("")
    # retranslateUi

