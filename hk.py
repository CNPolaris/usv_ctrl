# coding=utf-8

import os
import platform
import cv2
import numpy as np

from PySide6 import QtCore
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QMainWindow, QApplication

from utils.HCNetSDK import *
from utils.PlayCtrl import *

from ui import ui_hk


class HKVideo(QtCore.QThread):
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
            os.chdir(r'./sdk/win')
            self.Objdll = ctypes.CDLL(r'./HCNetSDK.dll')  # 加载网络库
            self.Playctrldll = ctypes.CDLL(r'./PlayCtrl.dll')  # 加载播放库
        else:
            os.chdir(r'./sdk/linux')
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
            lRealPlayHandle = self.open_preview(self.funcRealDataCallBack_V30)
            if lRealPlayHandle < 0:
                print('Open preview fail, error code is: %d' % self.Objdll.NET_DVR_GetLastError())
                # 登出设备
                self.Objdll.NET_DVR_Logout(lUserId)
                # 释放资源
                self.Objdll.NET_DVR_Cleanup()
                exit()
        except:
            pass


class HK_Window(QMainWindow):
    def __init__(self):
        super(HK_Window, self).__init__()
        self.ui = ui_hk.Ui_MainWindow()
        self.ui.setupUi(self)
        self.hk = HKVideo()

        self.hk.send_img_data.connect(self.recv_img)
        self.ui.pushButton.clicked.connect(self.open_hk)

    def recv_img(self, array, w, h):
        # img_rgb = cv2.cvtColor(array, cv2.COLOR_YUV2BGR_YV12)
        # img = QImage(array, array.shape[1], array[0], QImage.Format_RGB888)
        #
        # self.ui.video.setPixmap(QPixmap.fromImage(img))
        show = cv2.resize(array, (w, h))
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        showImage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)

        self.ui.video.setPixmap(QPixmap.fromImage(showImage))

    def open_hk(self):
        self.hk.start()


if __name__ == '__main__':
    # test = HKVideo()
    # test.open_win()
    app = QApplication(sys.argv)
    hk_win = HK_Window()
    hk_win.show()
    sys.exit(app.exec())
