"""
将GPS数据处理成ShapeFile文件
"""
import os
import geopandas as gp
from shapely import geometry

from libs import transform_degree, convert_to_baidu_single, convert_to_tencent_single


def gps_to_shp(path, processed=True, shape='line', baidu=False, tencent=False):
    """将GPS数据处理成矢量文件

    Parameters
    ----------
    path: str
        GPS数据路径, 以txt形式保存, 格式为 纬度,经度; 每个坐标点以分号分隔
    processed: bool, default True
        是否是标准的十进制度数, by default True
    shape: str, default line
        目标要素形状
            line: 线性 poly: 面 point: 点 multi: 复合面
    baidu: bool, default False
        是否转换成百度地图坐标, by default False
    tencent: bool, default False
        是否转成成腾讯地图坐标, by default False
    
    Returns
    -------
    shape: GeoDataFrame
        处理后的矢量元素
    bounds: list or tuple
        元素的边界,[lng_min, lat_min, lng_max, lat_max]
    """
    if os.path.exists(path):
        raise Exception('GPS file is not exists!!!')

    x_max, x_min, y_min, y_max = float('-inf'), float('inf'), float('inf'), float('-inf')
    points = []
    with open(path) as f:
        data = f.read()
    f.close()

    for xy in data.split(';'):
        y, _, x = xy.partition(',')
        x = float(x.strip())
        y = float(y.strip())

        if not processed:
            x = transform_degree(x)
            y = transform_degree(x)

        if baidu:
            x, y = convert_to_baidu_single(x, y)
        if tencent:
            x, y = convert_to_tencent_single(x, y)
        # 边界
        if x > x_max:
            x_max = x
        if x < x_min:
            x_min = x
        if y > y_max:
            y_max = y
        if y < y_min:
            y_min = y

        points.append(geometry.Point(x, y))
    if shape == 'line':
        return geometry.linestring(points), [x_min, y_min, x_max, y_max]
    elif shape == 'poly':
        return geometry.Polygon(points), [x_min, y_min, x_max, y_max]
    elif shape == 'point':
        return geometry.Point(points), [x_min, y_min, x_max, y_max]
    elif shape == 'multi':
        return geometry.MultiPolygon(points), [x_min, y_min, x_max, y_max]
