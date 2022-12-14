"""
-------------------------------------------------
File Name: main
Description:
Author: TianXin
Date：2022-11-29
-------------------------------------------------
"""
import ctypes
import os
import sys

import PySide6
import cv2
from PySide6 import QtCore
from PySide6.QtGui import QIcon, QImage, QPixmap
from PySide6.QtSerialPort import QSerialPort, QSerialPortInfo
from PySide6.QtCore import Slot
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtWebEngineCore import QWebEngineSettings
from PySide6.QtWidgets import *

from core.route import RouteThread
from core.udp_server import UDP_Thread
from core.video_web import VideoWebThread
from core.hk import HKVideoThread
from ui.ui_app import Ui_MainWindow
from mock.ship_info import ShipInfo
from utils.logger import logger

showMessage = QMessageBox.question
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")


class Window(QMainWindow):
    # 主线程向udp线程传参
    udp_params = QtCore.Signal(list)
    clients = QtCore.Signal(tuple)
    img_data = QtCore.Signal(object)
    # 监控信号
    up_signal = QtCore.Signal(int)
    down_signal = QtCore.Signal(int)
    left_signal = QtCore.Signal(int)
    right_signal = QtCore.Signal(int)
    up_left_signal = QtCore.Signal(int)
    up_right_signal = QtCore.Signal(int)
    down_left_signal = QtCore.Signal(int)
    down_right_signal = QtCore.Signal(int)
    zoom_in_signal = QtCore.Signal(int)
    zoom_out_signal = QtCore.Signal(int)
    pan_auto_signal = QtCore.Signal(int)
    # 主线程向路径规划线程传递数据
    route_bounds = QtCore.Signal(list)
    start_end = QtCore.Signal(list)
    route_accuracy = QtCore.Signal(int)
    check_point_lake = QtCore.Signal(list)

    def __init__(self):
        super().__init__()
        self.cur_dir = os.getcwd().replace('\\', '/')
        # UI载入
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # 初始化地图
        self.page = self.ui.webEngineView.page()
        self.ui.webEngineView.page().settings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        self.ui.webEngineView.page().settings().setAttribute(QWebEngineSettings.LocalContentCanAccessFileUrls, True)
        self.ui.webEngineView.page().settings().setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
        self.init_baidu()
        # UDP参数
        self.pause = False
        # 数据接收主线程
        self.udp = UDP_Thread()
        self.hk = HKVideoThread()
        self.video = VideoWebThread()
        self.route_thread = RouteThread()
        """
        GPS数据接收
        """
        # 主线程向udp子线程传参
        self.udp_params.connect(self.udp.udp_params_update)
        self.clients.connect(self.udp.add_client)
        # udp子线程向主线程传递
        self.udp.send_data.connect(self.log_list_view)
        self.udp.send_data.connect(self.send_coord_to_map)
        """
        视频监控线程
        """
        # 主线程与监控线程通信
        self.hk.send_img_data.connect(self.recv_img)
        self.up_signal.connect(self.hk.move_top)
        self.down_signal.connect(self.hk.move_down)
        self.left_signal.connect(self.hk.pan_left)
        self.right_signal.connect(self.hk.pan_right)
        self.up_left_signal.connect(self.hk.up_left)
        self.up_right_signal.connect(self.hk.up_right)
        self.down_left_signal.connect(self.hk.down_left)
        self.down_right_signal.connect(self.hk.down_right)
        self.zoom_in_signal.connect(self.hk.zoom_in)
        self.zoom_out_signal.connect(self.hk.zoom_out)
        self.pan_auto_signal.connect(self.hk.pan_auto)
        # 主线程向视频推流线程传值
        self.img_data.connect(self.video.recv_img)
        """
        路径规划线程
        """
        # 栅格精度
        self.ui.accuracy_text.setText('5')
        # 主线程向路径规划线程传值
        self.route_bounds.connect(self.route_thread.gen_grid)
        self.start_end.connect(self.route_thread.set_start_end)
        self.route_accuracy.connect(self.route_thread.set_accuracy)
        self.check_point_lake.connect(self.route_thread.check_in_lake)
        # route子线程向主线程传递
        self.route_thread.send_route_path.connect(self.send_path_to_map)
        self.route_thread.check_lake_signal.connect(self.check_point_before_route)
        # 路径规划线程
        self.route_thread.start()
        """
        参数
        """
        self.home = []
        self.startPoint = []  # 起点
        self.endPoint = []  # 终点
        self.com = QSerialPort()
        self.com_list = []
        self.current_client_type = 'UDP'
        self.ship_info = []  # 船的有关信息
        self.way_points = []  # 航点
        self.root_path = os.getcwd().replace("\\", "/")
        # 地图栅格化数据
        self.grid = None
        self.params = None
        self.grid_array = None
        self.bounds = []
        self.route = []
        """
        控件初始化
        """
        # btn
        self.ui.connect_btn.clicked.connect(self.on_connect_btn_clicked)
        self.ui.over_btn.clicked.connect(self.on_over_btn_clicked)
        self.ui.add_client_btn.clicked.connect(self.on_add_client_btn_clicked)
        self.ui.over_btn.setEnabled(False)
        self.ui.route_btn.clicked.connect(self.on_route_btn_clicked)
        # client and server
        self.ui.baud_label.setVisible(False)
        self.ui.com_label.setVisible(False)
        self.ui.client_serial_port.setVisible(False)
        self.ui.client_baud.setVisible(False)
        self.ui.ip_text.setText('127.0.0.1')
        self.ui.port_text.setText('9999')
        self.ui.client_ip_text.setText('127.0.0.1')
        self.ui.client_port_text.setText('8888')
        # log list View
        self.coords = []
        self.log_list_model = QtCore.QStringListModel(self.coords)
        self.ui.logList.setModel(self.log_list_model)
        # clients
        self.client_list = []  # 保存UDP连接的终端ip和port
        self.client_model = QtCore.QStringListModel(self.client_list)
        self.ui.client_listView.setModel(self.client_model)
        self.ui.client_listView.doubleClicked.connect(self.delete_clients_list_view)
        # the comboBox of map types
        self.map_types = ['百度地图', '高德地图', '腾讯地图', '天地图']
        self.map_html = ['baidu', 'gaode', 'tencent', 'tiandi']
        self.ui.mapType_comboBox.addItems(self.map_types)
        self.ui.mapType_comboBox.currentIndexChanged[int].connect(self.on_map_types_comboBox_changed)
        # the comboBox of client connect type
        self.client_connect_types = ['UDP', 'TCP', 'COM']
        self.ui.connect_types_comboBox.addItems(self.client_connect_types)
        self.ui.connect_types_comboBox.currentIndexChanged[int].connect(self.on_client_connect_comboBox_changed)
        self.ui.client_serial_port.currentIndexChanged[int].connect(self.on_client_serial_port_changed)
        # waypoints table 初始化
        self.init_way_points_table()
        """
        云台控制相关
        """
        # 初始化云台控制
        self.init_ctrl_btn()
        # 连接
        self.connect_flag = True
        self.ui.pan_auto_btn.clicked.connect(self.on_pan_auto_btn_clicked)
        # self.open_hk()
        self.ui.connect_btn_2.clicked.connect(self.open_hk)
        # 云端推流 TODO:效率太低 问题很大
        self.upload_flag = False
        self.ui.upload_img_btn.clicked.connect(self.on_upload_img_btn_clicked)
        # 自动化控制
        self.auto_flag = False

    def init_baidu(self):
        """init_baidu 初始化地图
        """
        path = os.getcwd().replace('\\', '/') + "/templates/baidu.html"
        self.ui.webEngineView.load(QtCore.QUrl(path))

    def on_connect_btn_clicked(self):
        """点击开始接收udp坐标数据传输
        """
        print("开始接收数据")
        self.ui.connect_btn.setEnabled(False)
        self.ui.over_btn.setEnabled(True)
        self.ui.ip_text.setEnabled(False)
        self.ui.port_text.setEnabled(False)
        self.pause = False
        self.update_udp_params()
        self.udp.start()

    def on_over_btn_clicked(self):
        """点击结束接收udp数据
        """
        print("终止接收数据")
        self.ui.connect_btn.setEnabled(True)
        self.ui.over_btn.setEnabled(False)
        self.ui.ip_text.setEnabled(True)
        self.ui.port_text.setEnabled(True)
        # 清除航迹
        self.page.runJavaScript('clearAllPath()')
        self.pause = True
        self.update_udp_params()

    def on_add_client_btn_clicked(self):
        """点击添加新的终端接收
        """
        print("添加新终端")
        if self.current_client_type == 'UDP':
            self.update_client()
        elif self.current_client_type == 'COM':
            port_name = self.com_list[self.ui.client_serial_port.currentIndex()].portName()
            baud_rate = self.com_list[self.ui.client_serial_port.currentIndex()].standardBaudRates()[
                self.ui.client_baud.currentIndex()]
            self.com.setPortName(str(port_name))
            self.com.setBaudRate(int(baud_rate))
            if self.com.open(QtCore.QIODevice.ReadOnly) == False:
                print(f'Open {port_name},baudRate {baud_rate} Port Failed')

    def update_udp_params(self):
        """udp数据监听服务器参数更新
        """
        params = [self.ui.ip_text.toPlainText(), int(self.ui.port_text.toPlainText()), self.pause]
        self.udp_params.emit(params)

    def update_client(self):
        """update_client 添加终端
        """
        cli = (self.ui.client_ip_text.toPlainText(), int(self.ui.client_port_text.toPlainText()))
        is_add = True
        if f'IP:{cli[0]},Port:{cli[1]}' not in self.client_list:
            ship = ShipInfo(ip=cli[0], port=cli[1], connect_type='UDP')
            self.ship_info.append(ship)
            self.page.runJavaScript(f'addNewShip({ship.get_ship_info()})')
            self.client_list.append(f'IP:{cli[0]},Port:{cli[1]}')
            self.client_model.setStringList(self.client_list)
            self.ui.client_listView.setModel(self.client_model)
            self.clients.emit(cli)
        else:
            QMessageBox.information(self, "添加终端", "该终端已经存在")

    def delete_clients_list_view(self):
        """终端列表移除某一项
        Returns
        -------

        """
        selected = self.ui.client_listView.selectedIndexes()
        index = selected[0].row()
        reply = showMessage(self, "终端列表", f"是否要删除终端{self.client_list[index]}",
                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            del self.client_list[index]
            self.client_model.setStringList(self.client_list)
            self.ui.client_listView.setModel(self.client_model)

    def log_list_view(self, addr, coord):
        self.coords.append(f'addr:{addr},coord:{coord}')
        self.log_list_model.setStringList(self.coords)
        self.ui.logList.setModel(self.log_list_model)
        self.ui.logList.scrollToBottom()

    def send_coord_to_map(self, addr, coord):
        """send_coord_to_map 向地图js传递数据

        Parameters
        ----------
        addr : str
            终端地址
        coord : str
            实时坐标
        """
        for item in self.ship_info:
            if item.is_ship(addr):
                info = item.get_ship_info()
        self.page.runJavaScript(f'genCoordsLine({info}, {coord})')

    @Slot(str)
    def update_home_point(self, home):
        """update_home_point 更新home点

        Parameters
        ----------
        home : str
            home点坐标 lng,lat
        """
        x, y = home.split(',')
        logger.info(f'家:{x},{y}')
        self.home.append(float(x))
        self.home.append(float(y))

    @Slot(str, result=int)
    def set_start_point(self, point):
        """set_start_point 设置路径起点

        Parameters
        ----------
        point : str
            经纬度坐标 lng,lat

        Returns
        -------
        result: int
            1: set start point successful
            0: set start point unsuccessful

        """
        x, y = point.split(',')
        logger.info(f'起点:{x},{y}')
        self.startPoint = [float(x), float(y)]
        return 1

    @Slot(str, result=int)
    def set_end_point(self, point):
        """set_end_point 设置路径终点

        Parameters
        ----------
        point : str
            经纬度坐标,以,分隔 lng,lat

        Returns
        -------
        result: int
            1: set end point successful
            0: set end point unsuccessful
        """
        x, y = point.split(',')
        logger.info(f'终点:{x},{y}')
        self.endPoint = [float(x), float(y)]
        return 1

    @Slot(str, result=int)
    def remove_start_end(self, t):
        if t == '0' or t == 0:
            logger.info(f"移除起点{self.startPoint}")
            self.startPoint = []
            return 1
        elif t == '1' or t == 1:
            logger.info(f"移除终点{self.endPoint}")
            self.endPoint = []
            return 1
        else:
            logger.info("移除起终点失败")
            return 0

    @Slot(str)
    def recv_way_point(self, point):
        """接收地图js传递来的手动打点路径坐标

        Parameters
        ----------
        point: str
            坐标点 [idx, lng, lat]

        Returns
        -------
        None
        """
        i, x, y = point.split(',')
        i = int(i)
        if len(self.way_points) - 1 < i:
            logger.info(f'添加航点:{i}, {x}, {y}')
            self.way_points.append([float(x), float(y)])
            row = self.ui.waypoints_table.rowCount()
            self.ui.waypoints_table.setRowCount(row + 1)
            self.ui.waypoints_table.setItem(row, 0, QTableWidgetItem(x))
            self.ui.waypoints_table.setItem(row, 1, QTableWidgetItem(y))
        else:
            logger.info(f'修改航点: {self.way_points[i]} -> ({i}, {x}, {y})')
            self.way_points[i] = [float(x), float(y)]
            self.ui.waypoints_table.setItem(i, 0, QTableWidgetItem(x))
            self.ui.waypoints_table.setItem(i, 1, QTableWidgetItem(y))

    def delete_way_point(self):
        selected = self.ui.waypoints_table.selectedIndexes()
        index = selected[0].row()
        reply = showMessage(self, "航点", f"是否移除航点{self.way_points[index]}",
                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            del self.way_points[index]
            self.ui.waypoints_table.removeRow(index)
            self.page.runJavaScript(f'removeWayPoint({index})')

    @Slot()
    def clear_way_points(self):
        """地图js清除全部航点时同步清除qt的航点数据
        """
        while self.ui.waypoints_table.rowCount() != 0:
            self.ui.waypoints_table.removeRow(0)
        logger.info(f'清除航点{self.way_points}')
        self.way_points = []

    @Slot(str)
    def recv_bounds(self, bounds):
        """接收地图js回传的研究区域边界坐标 左下点和右上点

        Parameters
        ----------
        bounds: str
            区域坐标: 'map,lng1,lat1,lng2,lat2',地图类型，左下角，右上角

        Returns
        -------

        """
        map, lng1, lat1, lng2, lat2 = bounds.split(',')
        lng1 = float(lng1)
        lat1 = float(lat1)
        lng2 = float(lng2)
        lat2 = float(lat2)
        self.bounds = [lng1, lat1, lng2, lat2]
        logger.info(f'研究区域为：{map}, {lng1},{lat1},{lng2},{lat2}')
        self.route_accuracy.emit(int(self.ui.accuracy_text.toPlainText()))
        self.route_bounds.emit(self.bounds)

    def check_point_before_route(self, flag):
        if not flag:
            QMessageBox.information(self, "Warn", "起点和终点需要在水域中")

    def on_route_btn_clicked(self):
        """开启路径规划btn绑定事件"""
        if len(self.startPoint) == 0 or len(self.endPoint) == 0:
            QMessageBox.information(self, "Warn", "请先确定起点和终点")
            pass
        elif int(self.ui.accuracy_text.toPlainText()) < 0:
            QMessageBox.information(self, "Warn", "栅格精确度不能小于0")
            pass
        elif self.route_thread.grid_array is None:
            QMessageBox.information(self, "Warn", "需要设置研究区域")
        else:
            self.check_point_lake.emit(self.startPoint)
            self.check_point_lake.emit(self.endPoint)
            self.start_end.emit([self.startPoint, self.endPoint])

    def send_path_to_map(self, path):
        """传递路劲规划坐标到地图js

        Parameters
        ----------
        path: list
            路径坐标列表: [(lng, lat)]

        Returns
        -------
        result: [{'lng': 0, 'lat': 0}]
        """
        temp = []
        for i in range(len(path)):
            temp.append({'lng': path[i][0], 'lat': path[i][1]})
        logger.info(f'最终路径: {temp}')
        self.page.runJavaScript(f'drawRoutePath({temp})')

    def on_map_types_comboBox_changed(self, i):
        """on_map_types_comboBox_changed 改变地图类型

        Parameters
        ----------
        i : int
            地图类型索引
        """
        # TODO实现地图类型切换
        print(i, self.map_types[i])
        html_path = self.root_path + "/templates/{0}.html".format(self.map_html[i])
        # with open(html_path, encoding='UTF-8') as f:
        #     html = f.read()
        # self.ui.webEngineView.setHtml(html)
        self.ui.webEngineView.load(QtCore.QUrl(html_path))

    def on_client_connect_comboBox_changed(self, i):
        """点击修改终端连接类型"""
        self.current_client_type = self.client_connect_types[i]
        if self.client_connect_types[i] == 'COM':
            self.com_list = QSerialPortInfo.availablePorts()
            self.ui.client_serial_port.clear()
            for i in self.com_list:
                self.ui.client_serial_port.addItem(i.portName())
            self.ui.baud_label.setVisible(True)
            self.ui.com_label.setVisible(True)
            self.ui.client_serial_port.setVisible(True)
            self.ui.client_baud.setVisible(True)
            self.ui.ip_label.setVisible(False)
            self.ui.client_ip_text.setVisible(False)
            self.ui.port_label.setVisible(False)
            self.ui.client_port_text.setVisible(False)
        else:
            self.com.close()
            self.ui.baud_label.setVisible(False)
            self.ui.com_label.setVisible(False)
            self.ui.client_serial_port.setVisible(False)
            self.ui.client_baud.setVisible(False)
            self.ui.ip_label.setVisible(True)
            self.ui.client_ip_text.setVisible(True)
            self.ui.port_label.setVisible(True)
            self.ui.client_port_text.setVisible(True)

    def on_client_serial_port_changed(self, port_index):
        bauds = self.com_list[port_index].standardBaudRates()
        for b in bauds:
            self.ui.client_baud.addItem(str(b))

    def on_back_home_btn_clicked(self):
        pass

    def init_ctrl_btn(self):
        """初始化云台控制控件"""
        self.ui.top_btn.setAutoRepeat(True)
        self.ui.top_btn.setAutoRepeatDelay(400)
        self.ui.top_btn.setAutoRepeatInterval(100)
        self.ui.top_btn.setIcon(QIcon("static/images/up.png"))
        self.ui.top_btn.pressed.connect(self.on_move_top_btn_pressed)
        self.ui.top_btn.released.connect(self.on_move_top_btn_released)

        self.ui.bottom_btn.setAutoRepeat(True)
        self.ui.bottom_btn.setAutoRepeatDelay(400)
        self.ui.bottom_btn.setAutoRepeatInterval(100)
        self.ui.bottom_btn.setIcon(QIcon("static/images/down.png"))
        self.ui.bottom_btn.pressed.connect(self.on_move_down_btn_pressed)
        self.ui.bottom_btn.released.connect(self.on_move_down_btn_released)

        self.ui.left_btn.setAutoRepeat(True)
        self.ui.left_btn.setAutoRepeatDelay(400)
        self.ui.left_btn.setAutoRepeatInterval(100)
        self.ui.left_btn.setIcon(QIcon("static/images/left.png"))
        self.ui.left_btn.pressed.connect(self.on_left_btn_pressed)
        self.ui.left_btn.released.connect(self.on_left_btn_released)

        self.ui.right_btn.setAutoRepeat(True)
        self.ui.right_btn.setAutoRepeatDelay(400)
        self.ui.right_btn.setAutoRepeatInterval(100)
        self.ui.right_btn.setIcon(QIcon("static/images/right.png"))
        self.ui.right_btn.pressed.connect(self.on_right_btn_pressed)
        self.ui.right_btn.released.connect(self.on_right_btn_released)

        self.ui.up_left_btn.setAutoRepeat(True)
        self.ui.up_left_btn.setAutoRepeatDelay(400)
        self.ui.up_left_btn.setAutoRepeatInterval(100)
        self.ui.up_left_btn.setIcon(QIcon("static/images/up_left.png"))
        self.ui.up_left_btn.pressed.connect(self.on_up_left_btn_pressed)
        self.ui.up_left_btn.released.connect(self.on_up_left_btn_released)

        self.ui.up_right_btn.setAutoRepeat(True)
        self.ui.up_right_btn.setAutoRepeatDelay(400)
        self.ui.up_right_btn.setAutoRepeatInterval(100)
        self.ui.up_right_btn.setIcon(QIcon("static/images/up_right.png"))
        self.ui.up_right_btn.pressed.connect(self.on_up_right_btn_pressed)
        self.ui.up_right_btn.released.connect(self.on_up_right_btn_released)

        self.ui.down_left_btn.setAutoRepeat(True)
        self.ui.down_left_btn.setAutoRepeatDelay(400)
        self.ui.down_left_btn.setAutoRepeatInterval(100)
        self.ui.down_left_btn.setIcon(QIcon("static/images/down_left.png"))
        self.ui.down_left_btn.pressed.connect(self.on_down_left_btn_pressed)
        self.ui.down_left_btn.released.connect(self.on_down_left_btn_released)

        self.ui.down_right_btn.setAutoRepeat(True)
        self.ui.down_right_btn.setAutoRepeatDelay(400)
        self.ui.down_right_btn.setAutoRepeatInterval(100)
        self.ui.down_right_btn.setIcon(QIcon("static/images/down_right.png"))
        self.ui.down_right_btn.pressed.connect(self.on_down_right_btn_pressed)
        self.ui.down_right_btn.released.connect(self.on_down_right_btn_released)

        self.ui.zoom_in_btn.setAutoRepeat(True)
        self.ui.zoom_in_btn.setAutoRepeatDelay(400)
        self.ui.zoom_in_btn.setAutoRepeatInterval(100)
        self.ui.zoom_in_btn.setIcon(QIcon("static/images/out.png"))
        self.ui.zoom_in_btn.pressed.connect(self.on_zoom_in_btn_pressed)
        self.ui.zoom_in_btn.released.connect(self.on_zoom_in_btn_released)

        self.ui.zoom_out_btn.setAutoRepeat(True)
        self.ui.zoom_out_btn.setAutoRepeatDelay(400)
        self.ui.zoom_out_btn.setAutoRepeatInterval(100)
        self.ui.zoom_out_btn.setIcon(QIcon("static/images/in.png"))
        self.ui.zoom_out_btn.pressed.connect(self.on_zoom_out_btn_pressed)
        self.ui.zoom_out_btn.released.connect(self.on_zoom_out_btn_released)

    def recv_img(self, array, w, h):
        """接收监控线程传递的图像流"""
        show = cv2.resize(array, (960, 640))
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        show_image = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)
        if self.upload_flag:
            ret, buffer = cv2.imencode('.jpg', show)
            self.img_data.emit(buffer.tobytes())
        self.ui.video.setPixmap(QPixmap.fromImage(show_image))

    def open_hk(self):
        """开启监控"""
        if self.connect_flag:
            self.hk.start()
            self.ui.connect_btn_2.setText("已连接")
            self.connect_flag = False
        else:
            self.connect_flag = True
            self.ui.connect_btn_2.setText("已断开")
            self.hk.destroy()

    def on_move_top_btn_pressed(self):
        self.up_signal.emit(0)

    def on_move_top_btn_released(self):
        self.up_signal.emit(1)

    def on_move_down_btn_pressed(self):
        self.down_signal.emit(0)

    def on_move_down_btn_released(self):
        self.down_signal.emit(1)

    def on_left_btn_pressed(self):
        self.left_signal.emit(0)

    def on_left_btn_released(self):
        self.left_signal.emit(1)

    def on_right_btn_pressed(self):
        self.right_signal.emit(0)

    def on_right_btn_released(self):
        self.right_signal.emit(1)

    def on_up_right_btn_pressed(self):
        self.up_right_signal.emit(0)

    def on_up_right_btn_released(self):
        self.up_right_signal.emit(1)

    def on_up_left_btn_pressed(self):
        self.up_left_signal.emit(0)

    def on_up_left_btn_released(self):
        self.up_left_signal.emit(1)

    def on_down_right_btn_pressed(self):
        self.down_right_signal.emit(0)

    def on_down_right_btn_released(self):
        self.down_right_signal.emit(1)

    def on_down_left_btn_pressed(self):
        self.down_left_signal.emit(0)

    def on_down_left_btn_released(self):
        self.down_left_signal.emit(1)

    def on_zoom_in_btn_pressed(self):
        self.zoom_in_signal.emit(0)

    def on_zoom_in_btn_released(self):
        self.zoom_in_signal.emit(1)

    def on_zoom_out_btn_pressed(self):
        self.zoom_out_signal.emit(0)

    def on_zoom_out_btn_released(self):
        self.zoom_out_signal.emit(1)

    def on_pan_auto_btn_clicked(self):
        if not self.auto_flag:
            self.pan_auto_signal.emit(0)
            self.auto_flag = True
            self.ui.pan_auto_btn.setText("STOP")
        else:
            self.pan_auto_signal.emit(1)
            self.ui.pan_auto_btn.setText("AUTO")
            self.auto_flag = False

    def closeEvent(self, event: PySide6.QtGui.QCloseEvent) -> None:
        reply = showMessage(self, '警告', "系统将退出，是否确认?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.hk.destroy()
            self.hk.exit(retcode=0)
            event.accept()
        else:
            event.ignore()

    def on_upload_img_btn_clicked(self):
        if not self.upload_flag:
            self.ui.upload_img_btn.setText("停止推流")
            self.video.start()
            self.upload_flag = True
        else:
            self.ui.upload_img_btn.setText("开始推流")
            self.video.exit(retcode=1)
            self.upload_flag = False

    def init_way_points_table(self):
        """初始化航点列表
        """
        self.ui.waypoints_table.setColumnCount(2)
        self.ui.waypoints_table.setHorizontalHeaderLabels(["经度", "纬度"])
        self.ui.waypoints_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.ui.waypoints_table.horizontalHeader().resizeSection(0, 154)
        self.ui.waypoints_table.horizontalHeader().resizeSection(1, 154)
        # 双击删除选中的航点
        self.ui.waypoints_table.doubleClicked.connect(self.delete_way_point)


def win():
    app = QApplication(sys.argv)
    channel = QWebChannel()

    w = Window()
    w.setWindowTitle("USV无人船控制系统")
    channel.registerObject('py', w)
    w.ui.webEngineView.page().setWebChannel(channel)
    w.ui.webEngineView.show()
    w.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    win()
