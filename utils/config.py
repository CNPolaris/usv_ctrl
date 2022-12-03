"""
-------------------------------------------------
   File Name: config
   Description:
   Author: tianxin
   Date：2022-11-06
   Ide: PyCharm
-------------------------------------------------
"""
import os
import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


class Config(object):
    def __init__(self):
        self.project_path = BASE_DIR + os.sep

    def get_log_path(self):
        """
        文件存在则返回，否则新建后返回
        :return: 文件路径：日期.log
        """
        log_path = self.project_path + "logs" + os.sep
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        return log_path + "{}.log".format(str(datetime.date.today()))


config = Config()
