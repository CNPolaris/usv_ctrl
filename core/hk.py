# coding=utf-8
"""
-------------------------------------------------
File Name: hk
Description: 该模块是实现对海康监控的云台控制线程
Author: TianXin
Date：2022-12-26
-------------------------------------------------
"""
import os
import platform
import PySide6
import cv2
import numpy as np

from PySide6 import QtCore
from PySide6.QtGui import QImage, QPixmap, QIcon
from PySide6.QtWidgets import QMainWindow, QApplication, QMessageBox

from utils.HCNetSDK import *
from utils.PlayCtrl import *
from ui import ui_hk

showMessage = QMessageBox.question
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")


class HKVideoThread(QtCore.QThread):
    send_img_data = QtCore.Signal(object, int, int)

    def __init__(self, ip='192.168.15.221', port=8000, username='admin', password='Just123!'):
        super().__init__()
        self.dev_ip = create_string_buffer(b'192.168.15.221')
        self.dev_port = port
        self.username = create_string_buffer(b'admin')
        self.password = create_string_buffer(b'Just123!')

        self.windows_flag = True
        self.funcRealDataCallBack_V30 = None
        self.Objdll = None  # 网络库
        self.PlayCtrl_Port = c_long(-1)  # 播放句柄
        self.Playctrldll = None  # 播放库
        self.FuncDecCB = None  # 播放库解码回调函数，需要定义为全局的
        self.lRealPlayHandle = None

        self.dev_info = None
        self.user_id = None
        self.cv = None

    def get_platform(self):
        sys_str = platform.system()
        if sys_str != "Windows":
            self.windows_flag = False

    def load_dll(self):
        # 加载库,先加载依赖库
        if self.windows_flag:
            os.chdir(r'../sdk/win')
            self.Objdll = ctypes.CDLL(r'./HCNetSDK.dll')  # 加载网络库
            self.Playctrldll = ctypes.CDLL(r'./PlayCtrl.dll')  # 加载播放库
        else:
            os.chdir(r'../sdk/linux')
            self.Objdll = cdll.LoadLibrary(r'./libhcnetsdk.so')
            self.Playctrldll = cdll.LoadLibrary(r'./libPlayCtrl.so')

    def set_sdk_init_cfg(self):

        if self.windows_flag:
            str_path = os.getcwd().encode('gbk')
            sdk_com_path = NET_DVR_LOCAL_SDK_PATH()
            sdk_com_path.sPath = str_path
            self.Objdll.NET_DVR_SetSDKInitCfg(2, byref(sdk_com_path))
            self.Objdll.NET_DVR_SetSDKInitCfg(3, create_string_buffer(str_path + b'\libcrypto-1_1-x64.dll'))
            self.Objdll.NET_DVR_SetSDKInitCfg(4, create_string_buffer(str_path + b'\libssl-1_1-x64.dll'))
        else:
            str_path = os.getcwd().encode('utf-8')
            sdk_com_path = NET_DVR_LOCAL_SDK_PATH()
            sdk_com_path.sPath = str_path
            self.Objdll.NET_DVR_SetSDKInitCfg(2, byref(sdk_com_path))
            self.Objdll.NET_DVR_SetSDKInitCfg(3, create_string_buffer(str_path + b'/libcrypto.so.1.1'))
            self.Objdll.NET_DVR_SetSDKInitCfg(4, create_string_buffer(str_path + b'/libssl.so.1.1'))

    def login_dev(self, Objdll):
        self.dev_info = NET_DVR_DEVICEINFO_V30()
        self.user_id = self.Objdll.NET_DVR_Login_V30(self.dev_ip, self.dev_port, self.username, self.password,
                                                     byref(self.dev_info))
        return self.user_id, self.dev_info

    def dec_CB_fun(self, nPort, pBuf, nSize, pFrameInfo, nUser, nReserved2):
        # 解码回调函数
        if pFrameInfo.contents.nType == 3:
            # 解码返回视频YUV数据，将YUV数据转成cv
            nWidth = pFrameInfo.contents.nWidth
            nHeight = pFrameInfo.contents.nHeight
            dwFrameNum = pFrameInfo.contents.dwFrameNum
            nStamp = pFrameInfo.contents.nStamp
            YUV = np.frombuffer(pBuf[:nSize], dtype=np.uint8)
            YUV = np.reshape(YUV, [nHeight + nHeight // 2, nWidth])
            img_rgb = cv2.cvtColor(YUV, cv2.COLOR_YUV2BGR_YV12)
            self.send_img_data.emit(img_rgb, nWidth, nHeight)

    def real_data_callback_v30(self, lPlayHandle, dwDataType, pBuffer, dwBufSize, pUser):
        # 码流回调
        if dwDataType == NET_DVR_SYSHEAD:
            print(f'{lPlayHandle}, {pBuffer}, {dwBufSize}')
            self.Playctrldll.PlayM4_SetStreamOpenMode(self.PlayCtrl_Port, 0)
            if self.Playctrldll.PlayM4_OpenStream(self.PlayCtrl_Port, pBuffer, dwBufSize, 1024 * 1024):
                self.FuncDecCB = DECCBFUNWIN(self.dec_CB_fun)
                self.Playctrldll.PlayM4_SetDecCallBackExMend(self.PlayCtrl_Port, self.FuncDecCB, None, 0, None)

            if self.Playctrldll.PlayM4_Play(self.PlayCtrl_Port):
                print(u'调用播放库成功')
            else:
                print(u'调用播放库失败')

        elif dwDataType == NET_DVR_STREAMDATA:
            self.Playctrldll.PlayM4_InputData(self.PlayCtrl_Port, pBuffer, dwBufSize)
        else:
            print(u'其他数据, 长度', dwBufSize)

    def open_preview(self, call_back_fun):
        preview_info = NET_DVR_PREVIEWINFO()
        preview_info.hPlayWnd = 0
        preview_info.lChannel = 1
        preview_info.dwStreamType = 0
        preview_info.dwLinkeMode = 0
        preview_info.bBlocked = 1

        lRealPlayHandle = self.Objdll.NET_DVR_RealPlay_V40(self.user_id, byref(preview_info), call_back_fun, None)
        return lRealPlayHandle

    def input_data(self, fileMp4):
        while True:
            p_file_data = fileMp4.read(4096)
            if p_file_data is None:
                break
            if not self.Playctrldll.PlayM4_InputData(self.PlayCtrl_Port, p_file_data, len(p_file_data)):
                break

    def move_top(self, signal):
        lRet = self.Objdll.NET_DVR_PTZControl(self.lRealPlayHandle, TILT_UP, signal)
        if lRet == 0:
            print('Start ptz control fail, error code is: %d' % self.Objdll.NET_DVR_GetLastError())
        else:
            print('Start ptz control success')

    def move_down(self, signal):
        lRet = self.Objdll.NET_DVR_PTZControl(self.lRealPlayHandle, TILT_DOWN, signal)
        if lRet == 0:
            print('Start ptz control fail, error code is: %d' % self.Objdll.NET_DVR_GetLastError())
        else:
            print('Start ptz control success')

    def pan_left(self, signal):
        lRet = self.Objdll.NET_DVR_PTZControl(self.lRealPlayHandle, PAN_LEFT, signal)
        if lRet == 0:
            print('Start ptz control fail, error code is: %d' % self.Objdll.NET_DVR_GetLastError())
        else:
            print('Start ptz control success')

    def pan_right(self, signal):
        lRet = self.Objdll.NET_DVR_PTZControl(self.lRealPlayHandle, PAN_RIGHT, signal)
        if lRet == 0:
            print('Start ptz control fail, error code is: %d' % self.Objdll.NET_DVR_GetLastError())
        else:
            print('Start ptz control success')

    def up_left(self, signal):
        lRet = self.Objdll.NET_DVR_PTZControl(self.lRealPlayHandle, UP_LEFT, signal)
        if lRet == 0:
            print('Start ptz control fail, error code is: %d' % self.Objdll.NET_DVR_GetLastError())
        else:
            print('Start ptz control success')

    def up_right(self, signal):
        lRet = self.Objdll.NET_DVR_PTZControl(self.lRealPlayHandle, UP_RIGHT, signal)
        if lRet == 0:
            print('Start ptz control fail, error code is: %d' % self.Objdll.NET_DVR_GetLastError())
        else:
            print('Start ptz control success')

    def down_left(self, signal):
        lRet = self.Objdll.NET_DVR_PTZControl(self.lRealPlayHandle, DOWN_LEFT, signal)
        if lRet == 0:
            print('Start ptz control fail, error code is: %d' % self.Objdll.NET_DVR_GetLastError())
        else:
            print('Start ptz control success')

    def down_right(self, signal):
        lRet = self.Objdll.NET_DVR_PTZControl(self.lRealPlayHandle, DOWN_RIGHT, signal)
        if lRet == 0:
            print('Start ptz control fail, error code is: %d' % self.Objdll.NET_DVR_GetLastError())
        else:
            print('Start ptz control success')

    def pan_auto(self, signal):
        lRet = self.Objdll.NET_DVR_PTZControl(self.lRealPlayHandle, PAN_AUTO, signal)
        if lRet == 0:
            print('Start ptz control fail, error code is: %d' % self.Objdll.NET_DVR_GetLastError())
        else:
            print('Start ptz control success')

    def zoom_in(self, signal):
        lRet = self.Objdll.NET_DVR_PTZControl(self.lRealPlayHandle, ZOOM_IN, signal)
        if lRet == 0:
            print('Start ptz control fail, error code is: %d' % self.Objdll.NET_DVR_GetLastError())
        else:
            print('Start ptz control success')

    def zoom_out(self, signal):
        lRet = self.Objdll.NET_DVR_PTZControl(self.lRealPlayHandle, ZOOM_OUT, signal)
        if lRet == 0:
            print('Start ptz control fail, error code is: %d' % self.Objdll.NET_DVR_GetLastError())
        else:
            print('Start ptz control success')

    def destroy(self):
        self.Objdll.NET_DVR_StopRealPlay(self.lRealPlayHandle)
        if self.PlayCtrl_Port.value > -1:
            self.Playctrldll.PlayM4_Stop(self.PlayCtrl_Port)
            self.Playctrldll.PlayM4_CloseStream(self.PlayCtrl_Port)
            self.Playctrldll.PlayM4_FreePort(self.PlayCtrl_Port)
            self.PlayCtrl_Port = c_long(-1)
        self.Objdll.NET_DVR_Logout(self.user_id)
        self.Objdll.NET_DVR_Cleanup()
        print("资源释放")

    def run(self) -> None:
        try:
            self.get_platform()
            self.load_dll()
            self.set_sdk_init_cfg()
            #
            self.Objdll.NET_DVR_Init()
            # # 启用SDK写日志
            self.Objdll.NET_DVR_SetLogToFile(3, bytes('./SdkLog_Python/', encoding="utf-8"), False)
            #
            if not self.Playctrldll.PlayM4_GetPort(byref(self.PlayCtrl_Port)):
                print(u'获取播放库句柄失败')
            #
            # 登录设备
            (lUserId, device_info) = self.login_dev(self.Objdll)
            if lUserId < 0:
                err = self.Objdll.NET_DVR_GetLastError()
                print('Login device fail, error code is: %d' % self.Objdll.NET_DVR_GetLastError())
                # 释放资源
                self.Objdll.NET_DVR_Cleanup()
                exit()
            #
            self.funcRealDataCallBack_V30 = REALDATACALLBACK(self.real_data_callback_v30)
            self.lRealPlayHandle = self.open_preview(self.funcRealDataCallBack_V30)
            if self.lRealPlayHandle < 0:
                print('Open preview fail, error code is: %d' % self.Objdll.NET_DVR_GetLastError())
                # 登出设备
                self.Objdll.NET_DVR_Logout(lUserId)
                # 释放资源
                self.Objdll.NET_DVR_Cleanup()
                exit()
        except:
            pass


class HK_Window(QMainWindow):
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

    def __init__(self):
        super(HK_Window, self).__init__()
        self.ui = ui_hk.Ui_MainWindow()
        self.ui.setupUi(self)
        self.hk = HKVideoThread()
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
        # 设置图片大小
        self.width = self.ui.video.geometry().width()
        self.height = self.ui.video.geometry().height()

        print(self.size)
        # 初始化云台控制
        self.init_ctrl_btn()
        # 连接
        self.connect_flag = True
        self.ui.pan_auto_btn.clicked.connect(self.on_pan_auto_btn_clicked)
        self.open_hk()
        self.ui.connect_btn.clicked.connect(self.open_hk)
        # 自动化控制
        self.auto_flag = False

    def init_ctrl_btn(self):
        # 云台控制
        self.ui.top_btn.setAutoRepeat(True)
        self.ui.top_btn.setAutoRepeatDelay(400)
        self.ui.top_btn.setAutoRepeatInterval(100)
        self.ui.top_btn.setIcon(QIcon("../static/images/up.png"))
        self.ui.top_btn.pressed.connect(self.on_move_top_btn_pressed)
        self.ui.top_btn.released.connect(self.on_move_top_btn_released)

        self.ui.bottom_btn.setAutoRepeat(True)
        self.ui.bottom_btn.setAutoRepeatDelay(400)
        self.ui.bottom_btn.setAutoRepeatInterval(100)
        self.ui.bottom_btn.setIcon(QIcon("../static/images/down.png"))
        self.ui.bottom_btn.pressed.connect(self.on_move_down_btn_pressed)
        self.ui.bottom_btn.released.connect(self.on_move_down_btn_released)

        self.ui.left_btn.setAutoRepeat(True)
        self.ui.left_btn.setAutoRepeatDelay(400)
        self.ui.left_btn.setAutoRepeatInterval(100)
        self.ui.left_btn.setIcon(QIcon("../static/images/left.png"))
        self.ui.left_btn.pressed.connect(self.on_left_btn_pressed)
        self.ui.left_btn.released.connect(self.on_left_btn_released)

        self.ui.right_btn.setAutoRepeat(True)
        self.ui.right_btn.setAutoRepeatDelay(400)
        self.ui.right_btn.setAutoRepeatInterval(100)
        self.ui.right_btn.setIcon(QIcon("../static/images/right.png"))
        self.ui.right_btn.pressed.connect(self.on_right_btn_pressed)
        self.ui.right_btn.released.connect(self.on_right_btn_released)

        self.ui.up_left_btn.setAutoRepeat(True)
        self.ui.up_left_btn.setAutoRepeatDelay(400)
        self.ui.up_left_btn.setAutoRepeatInterval(100)
        self.ui.up_left_btn.setIcon(QIcon("../static/images/up_left.png"))
        self.ui.up_left_btn.pressed.connect(self.on_up_left_btn_pressed)
        self.ui.up_left_btn.released.connect(self.on_up_left_btn_released)

        self.ui.up_right_btn.setAutoRepeat(True)
        self.ui.up_right_btn.setAutoRepeatDelay(400)
        self.ui.up_right_btn.setAutoRepeatInterval(100)
        self.ui.up_right_btn.setIcon(QIcon("../static/images/up_right.png"))
        self.ui.up_right_btn.pressed.connect(self.on_up_right_btn_pressed)
        self.ui.up_right_btn.released.connect(self.on_up_right_btn_released)

        self.ui.down_left_btn.setAutoRepeat(True)
        self.ui.down_left_btn.setAutoRepeatDelay(400)
        self.ui.down_left_btn.setAutoRepeatInterval(100)
        self.ui.down_left_btn.setIcon(QIcon("../static/images/down_left.png"))
        self.ui.down_left_btn.pressed.connect(self.on_down_left_btn_pressed)
        self.ui.down_left_btn.released.connect(self.on_down_left_btn_released)

        self.ui.down_right_btn.setAutoRepeat(True)
        self.ui.down_right_btn.setAutoRepeatDelay(400)
        self.ui.down_right_btn.setAutoRepeatInterval(100)
        self.ui.down_right_btn.setIcon(QIcon("../static/images/down_right.png"))
        self.ui.down_right_btn.pressed.connect(self.on_down_right_btn_pressed)
        self.ui.down_right_btn.released.connect(self.on_down_right_btn_released)

        self.ui.zoom_in_btn.setAutoRepeat(True)
        self.ui.zoom_in_btn.setAutoRepeatDelay(400)
        self.ui.zoom_in_btn.setAutoRepeatInterval(100)
        self.ui.zoom_in_btn.setIcon(QIcon("../static/images/out.png"))
        self.ui.zoom_in_btn.pressed.connect(self.on_zoom_in_btn_pressed)
        self.ui.zoom_in_btn.released.connect(self.on_zoom_in_btn_released)

        self.ui.zoom_out_btn.setAutoRepeat(True)
        self.ui.zoom_out_btn.setAutoRepeatDelay(400)
        self.ui.zoom_out_btn.setAutoRepeatInterval(100)
        self.ui.zoom_out_btn.setIcon(QIcon("../static/images/in.png"))
        self.ui.zoom_out_btn.pressed.connect(self.on_zoom_out_btn_pressed)
        self.ui.zoom_out_btn.released.connect(self.on_zoom_out_btn_released)

    def recv_img(self, array, w, h):
        show = cv2.resize(array, (960, 640))
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        show_image = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)

        self.ui.video.setPixmap(QPixmap.fromImage(show_image))

    def open_hk(self):
        if self.connect_flag:
            self.hk.start()
            self.ui.connect_btn.setText("已连接")
            self.connect_flag = False
        else:
            self.connect_flag = True
            self.ui.connect_btn.setText("已断开")
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    hk_win = HK_Window()
    hk_win.show()
    sys.exit(app.exec())
