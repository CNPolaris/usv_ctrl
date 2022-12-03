"""
数据处理库
"""
import os
from libs import transform_degree


def gps_processing(file_path, save_path=None, save_name=None):
    """GPS原始数据文件处理,并生成标准的数据格式

    Parameters
    ----------
    file_path: string
        文件存储路径
    save_path: string, default None
        结果保存路径
    save_name: string, default haiyunhu
        保存文件名
    """
    if not os.path.exists(file_path):
        raise Exception('File not exists')
    if save_path is None:
        save_path = os.path.abspath(__file__)
    if save_name is None:
        save_name = 'haiyunhu'

    f = open(file_path, 'r')
    lines = f.readlines()

    result = []
    for line in lines:
        strs = line.split(',')
        if strs[0] == '"$GPGGA':
            result.append('{0},{1}'.format(transform_degree(strs[2]), transform_degree(strs[4])))
        else:
            continue
    t = open(save_path + os.sep + '{0}.txt'.format(save_name), 'w')
    t.write(';'.join(result))
    t.close()


def island_processing(file_path, save_path=None, save_name=None):
    """针对浮岛数据进行处理

    Parameters
    ----------
    file_path:string
        文件路径
    save_path:string, default None
        结果保存路径
    save_name: optional, default None
        保存文件名, by default None
    """
    if not os.path.exists(file_path):
        raise Exception('File not exists')
    if save_path is None:
        save_path = os.path.abspath(__file__)
    if save_name is None:
        save_name = 'island'
    with open(file_path) as f:
        data = f.read()
    f.close()

    result = []
    for xy in data.split(';'):
        y, _, x = xy.partition(',')
        x = transform_degree(float(x.strip()))
        y = transform_degree(float(y.strip()))
        result.append('{0},{1}'.format(y, x))
    t = open(save_path + os.sep + '{0}.txt'.format(save_name), 'w')
    t.write(';'.join(result))
    t.close()


# if __name__ == '__main__':
#     save_path_ = 'E:\\just\\海韵湖智能技术实验场\\原始数据\\processed'
#     file_path_ = 'E:\\just\\海韵湖智能技术实验场\\原始数据\\data\\环湖原始数据.txt'
#     name = 'lake'
#     gps_processing(file_path_, save_path_, name)
#     island_path = 'E:\\just\\海韵湖智能技术实验场\\原始数据\\data\\浮岛数据.txt'
#     island_processing(island_path, save_path_, 'island')
