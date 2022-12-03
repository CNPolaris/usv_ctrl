"""
-------------------------------------------------
File Name: convert
Description: GPS坐标处理工具库
Author: tianxin
Date: 2022-10-27
-------------------------------------------------
"""
import re
import requests
import geopandas as gp
from shapely import geometry
import math

BAIDU_KEY = 'W5yIofKvMmzRODHonVBAx9h3aGd57kEN'
TENCENT_KEY = 'WEIBZ-CNUKX-2RM4N-Z7OXX-WAF3Z-SKFB5'


def convert_to_baidu_single(lng, lat):
    """单个标准GPS坐标转换成百度地图坐标

    Parameters
    ----------
    lng: float or str
        经度
    lat: float or str
        纬度

    Examples
    --------
    >>> convert_to_baidu(119.2173359, 32.0693007)
    >>> [119.2292438054453, 32.07294333935913]
    type: list

    Returns
    -------
    [lng, lat]: list
        百度地图采用的经纬度坐标（bd09ll）[lng, lat]
    """
    try:
        url = 'https://api.map.baidu.com/geoconv/v1/?coords={0},{1}'.format(lng, lat) + '&from=1&to=5&ak={}'.format(
            BAIDU_KEY)
        re = requests.get(url).json()
        if re['status'] == 0:
            result = re['result'][0]
            return [result['x'], result['y']]
        else:
            return None
    except Exception as e:
        print(e)
        return None


def convert_by_baidu(coords, f=1, t=5):
    """通过百度API将标准GPS坐标转换成指定坐标类型
        源坐标类型：
            1：GPS标准坐标；
            2：搜狗地图坐标；
            3：火星坐标（gcj02），即高德地图、腾讯地图和MapABC等地图使用的坐标；
            4：3中列举的地图坐标对应的墨卡托平面坐标;
            5：百度地图采用的经纬度坐标（bd09ll）；
            6：百度地图采用的墨卡托平面坐标（bd09mc）;
            7：图吧地图坐标；
            8：51地图坐标；
        目标坐标类型：
            3：火星坐标（gcj02），即高德地图、腾讯地图及MapABC等地图使用的坐标；
            5：百度地图采用的经纬度坐标（bd09ll）；
            6：百度地图采用的墨卡托平面坐标（bd09mc）；

    Parameters
    ----------
    coords: list
        需转换的源坐标，多组坐标以“;”分隔
    f: int,default 1
        源坐标类型 in range(1, 9)
    t: int,default 5
        目标坐标类型 in [3, 5, 6]

    Examples
    --------
    >>> convert_by_baidu([[119.2173359, 32.0693007], [119.2171111, 32.0692883]])
    >>> [[119.2292438054453, 32.07294333935913], [119.22901934296017, 32.07293057976518]]
    type: list

    Returns
    -------
    result: list
        批量转换结果
    """
    try:
        if len(coords) > 50:
            print('To much coord, must be less than 50\n')
        if f not in range(1, 9):
            print('f must in 1 to 8')
        if t not in [3, 5, 6]:
            print('t must in [3, 5, 6]')

        temp_coords = ''
        last_index = len(coords)
        if last_index == 1:
            temp_coords = '{0},{1}'.format(coords[0][0], coords[0][1])
        else:
            for i in range(last_index - 1):
                temp_coords += '{0},{1};'.format(coords[i][0], coords[i][1])
            temp_coords += '{0},{1}'.format(coords[last_index - 1][0], coords[last_index - 1][1])

        url = 'https://api.map.baidu.com/geoconv/v1/?from={0}&to={1}&ak={2}&coords={3}'.format(
            f, t, BAIDU_KEY, temp_coords)
        re = requests.get(url).json()

        if re['status'] == 0:
            result = []
            for item in re['result']:
                result.append([item['x'], item['y']])
            return result
        else:
            return None
    except Exception as e:
        print(e)


def get_distance_by_baidu():
    url = 'https://api.map.baidu.com/api_trackanalysis/v1/roadgrade?'
    body = {}
    body['ak'] = BAIDU_KEY
    body['point_list'] = [
        {
            'latitude': 32.115410000000004,
            'coord_type_input': 'wgs84',
            'longitude': 119.36110833333332,
            'loc_time': 1632817534
        },
        {
            'latitude': 32.115410000000004,
            'coord_type_input': 'wgs84',
            'longitude': 119.36119833333332,
            'loc_time': 1632817592
        }
    ]
    print(body)
    re = requests.post(url=url, data=body).json()
    print(re)


def convert_to_tencent_single(lng, lat, t=2):
    """使用腾讯地图API转换坐标

    Parameters
    ----------
    lng: float or str
        经度
    lat: float or str
        纬度
    t: optional, default 2
        坐标类型
        
    Examples
    --------
    >>> convert_by_tencent([119.3609491,32.11607947])
    >>> [119.36638, 32.114192]
    type: list
    
    Returns
    -------
    coord: list
        转换完成的腾讯地图坐标
    """
    url = 'https://apis.map.qq.com/ws/coord/v1/translate?locations={0},{1}&type={2}&key={3}'.format(lat, lng,
                                                                                                    t, TENCENT_KEY)
    re = requests.get(url).json()
    if re['status'] == 0:
        locations = re['locations']
        return [locations[0]['lng'], locations[0]['lat']]
    return None


def convert_to_tencent(coords, t=2):
    """批量转换坐标至腾讯地图坐标

    Parameters
    ----------
    coords: list
        标准坐标
    t: optional
        _description_, by default 2
    
    Examples
    --------
    >>> convert_to_tencent([[119.2169042, 32.069362], [119.2169042, 32.069362]])
    >>> [[119.222193, 32.06735], [119.222193, 32.06735]]
    type:list

    Returns
    -------
    result: list
        转换后的坐标列表
    """
    try:
        locations = []
        for item in coords:
            locations.append('{0},{1}'.format(item[1], item[0]))
        url = 'https://apis.map.qq.com/ws/coord/v1/translate?locations={0}&type={1}&key={2}'.format(';'.join(locations),
                                                                                                    t, TENCENT_KEY)
        re = requests.get(url).json()
        if re['status'] == 0:
            result = []
            locations = re['locations']
            for i in locations:
                result.append([i['lng'], i['lat']])
            return result
        else:
            return None
    except Exception as e:
        print(e)


def gcj02_to_wgs84(lng, lat):
    """GCJ02格式坐标转WGS84格式

    Parameters
    ----------
    lng: float
        经度
    lat: float
        纬度

    Returns
    -------
    lng: float
        WGS84下经度
    lat: float
        WGS84下纬度
    """
    try:
        lng = lng.astype(float)
        lat = lat.astype(float)
    except Exception:
        lng = float(lng)
        lat = float(lat)

    d_lng = transform_lng(lng - 105.0, lat - 35.0)
    d_lat = transform_lat(lng - 105.0, lat - 35.0)
    rad_lat = lat / 180.0 * math.pi
    magic = math.sin(rad_lat)
    magic = 1 - math.e * magic * magic
    sqrt_magic = math.sqrt(magic)
    d_lat = (d_lat * 180.0) / ((6378245.0 * (1 - math.e)) / (magic * sqrt_magic) * math.pi)
    d_lng = (d_lng * 180.0) / (6378245.0 / sqrt_magic * math.cos(rad_lat) * math.pi)
    mg_lat = lat + d_lat
    mg_lng = lng + d_lng
    return lng * 2 - mg_lng, lat * 2 - mg_lat


def wgs84_to_gcj02(lng, lat):
    """WGS84坐标转GCJ02坐标

    Parameters
    ----------
    lng:float
        十进制经度
    lat:float
        十进制纬度

    Returns
    -------
    lng: float
        GCJ02下经度
    lat: float
        GCJ下纬度
    """
    try:
        lng = lng.astype(float)
        lat = lat.astype(float)
    except Exception:
        lng = float(lng)
        lat = float(lat)
    d_lat = transform_lat(lng - 105.0, lat - 35.0)
    d_lng = transform_lng(lng - 105.0, lat - 35.0)
    rad_lat = lat / 180.0 * math.pi
    magic = math.sin(rad_lat)
    magic = 1 - math.e * magic * magic
    sqrt_magic = math.sqrt(magic)
    d_lat = (d_lat * 180.0) / ((6378245.0 * (1 - math.e)) / (magic * sqrt_magic) * math.pi)
    d_lng = (d_lng * 180.0) / (6378245.0 / sqrt_magic * math.cos(rad_lat) * math.pi)
    mg_lat = lat + d_lat
    mg_lng = lng + d_lng
    return mg_lng, mg_lat


def transform_lat(lng, lat):
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + \
          0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * math.pi) + 20.0 *
            math.sin(2.0 * lng * math.pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * math.pi) + 40.0 *
            math.sin(lat / 3.0 * math.pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * math.pi) + 320 *
            math.sin(lat * math.pi / 30.0)) * 2.0 / 3.0
    return ret


def transform_lng(lng, lat):
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + \
          0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * math.pi) + 20.0 *
            math.sin(2.0 * lng * math.pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lng * math.pi) + 40.0 *
            math.sin(lng / 3.0 * math.pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lng / 12.0 * math.pi) + 300.0 *
            math.sin(lng / 30.0 * math.pi)) * 2.0 / 3.0
    return ret


def convert_from_gps_to_shp(save=False, path=None, filename=None, to=2):
    """将提取出的GPS数据转成shapefile文件

    Parameters
    ----------
    save: bool, default False
        if True, save to file
    path: string, default  E:\\just\\海韵湖智能技术实验场\\原始数据\\data\\环湖数据.txt
        GPS文件路径
    to: int, default 2
        要素维数 1：一维 2：二维
    filename: string, default 'haiyunhu'
        保存的文件名

    """
    try:
        if path is None:
            path = 'E:\\just\\海韵湖智能技术实验场\\原始数据\\data\\环湖数据.txt'
        if filename is None:
            filename = 'haiyunhu'
        points = []
        with open(path) as f:
            data = f.read()
        for xy in data.split(';'):
            y, _, x = xy.partition(',')
            x = transform_degree(float(x.strip()))
            y = transform_degree(float(y.strip()))
            points.append(geometry.Point(x, y))
        # 线性要素
        if to == 1:
            line_ = geometry.LineString(points)
            line = gp.GeoSeries(line_, crs='EPSG:4326')
            if save:
                line.to_file('{0}.shp', filename, driver='ESRI Shapefile', encoding='utf-8')
        # 面性要素
        if to == 2:
            poly_ = geometry.Polygon(points)
            poly = gp.GeoSeries(poly_, crs='EPSG:4326')
            if save:
                poly.to_file('{0}.shp'.format(filename), driver='ESRI Shapefile', encoding='utf-8')
    except Exception as e:
        print(e)


def degree_to_lng_lat(degree):
    """度分秒格式GPS数据转经纬度格式

    Parameters
    ----------
    degree: string
        41°8′32.01″ 类似这种格式

    Examples
    --------
    >>> degree_to_lng_lat('41°8′32.01″')
    >>> 41.142224999999996
    dtype: float

    Returns
    -------
    degree: float
        经纬度格式数据
    """
    degree_split = re.split(u'°|\′|\″', degree)[:3]
    if len(degree_split) == 3:
        x = [float(i) for i in degree_split]
        data = (x[0] + x[1] / 60 + x[2] / 3600)
        return float(data)


def transform_degree(degree):
    """GPS坐标转dd.mmmm格式
    纬度 度分 ddmm.mmmmm 转dd.ddddd
    经度 度分 dddmm.mmmmm 转 ddd.ddddd

    Parameters
    ----------
    degree: float
        ddmm.mmmm 或 dddmm.mmmm 格式的GPS数据

    Examples
    --------
    >>> transform_degree(3207.0930)
    >>> 32.11821666666666
    dtype: float
    >>> transform_degree(11921.6796)
    >>> 119.36132666666666
    dtype: float

    Returns
    --------
    degree: float
        十进制度数
    """
    if type(degree) == str:
        degree = float(degree)
    return int(degree / 100) + (degree % 100) / 60


def transform_shape(gdf, method):
    """对地理要素整体进行坐标转换

    Parameters
    ----------
    gdf: GeoDataFrame
        地理要素
    method: function
        使用的坐标转换函数

    Returns
    -------
    gdf: GeoDataFrame
        转换后的地理要素
    """
    if type(gdf) != gp.GeoDataFrame:
        raise Exception('The gdf type must GeoDataFrame, but the type is {}'.format(type(gdf)))
    from shapely.ops import transform
    gdf_result = gdf.copy()
    gdf_result['geometry'] = gdf_result['geometry'].apply(lambda r: transform(method, r))
    return gdf_result


def get_flatter_distance(coord1, coord2):
    """计算两个坐标点之间的距离，以list的形式输入两个左边点，[经度，纬度](十进制度数)
    Parameters
    ----------
    coord1: list or tuple or dict
        坐标点1
    coord2: list or tuple or dict
        坐标点2
        
    Examples
    --------
    >>> get_flatter_distance([119.36110833333332,32.115410000000004], [119.36119833333332,32.115410000000004])
    >>> 8.475771005324928
    type: float
    
    >>> get_flatter_distance((119.36110833333332,32.115410000000004), (119.36119833333332,32.115410000000004))
    >>> 8.475771005324928
    type: float

    Returns
    -------
    distance: float
        两个坐标点之间的距离
    """
    if type(coord1) == dict:
        coord1 = [coord1['lng'], coord1['lat']]
    if type(coord2) == dict:
        coord2 = [coord2['lng'], coord2['lat']]

    pi = math.pi  # PI
    double_pi = math.pi * 2  # double PI
    pi_for_180 = math.pi / 180.0  # PI/180.0
    radius_earth = 6371004  # radius of earth
    # 角度转换成弧度
    east_to_west_1, north_to_south_1 = coord1[0] * pi_for_180, coord1[1] * pi_for_180
    east_to_west_2, north_to_south_2 = coord2[0] * pi_for_180, coord2[1] * pi_for_180
    # 经度差
    dist_east_west = east_to_west_1 - east_to_west_2
    # 若跨东经和西经180度，进行调整
    if dist_east_west > pi:
        dist_east_west = double_pi - dist_east_west
    elif dist_east_west + pi < 0:
        dist_east_west = double_pi + dist_east_west
    # 东西方向长度（在纬度圈上的投影长度）
    dx = radius_earth * math.cos(north_to_south_1) * dist_east_west
    # 南北方向长度（在经度圈上的投影长度）
    dy = radius_earth * (north_to_south_1 - north_to_south_2)
    # 勾股定理求斜边长 单位：m
    distance = math.sqrt(dx ** 2 + dy ** 2)
    return distance


def get_distance(lng1, lat1, lng2, lat2):
    """经纬度换算距离
    按照经度1,纬度1,经度2,纬度2(十进制度数)输入, 获取距离米

    Parameters
    ----------
    lng1: float
        经度1
    lat1: float
        纬度1
    lng2: float
        经度2
    lat2: float
        纬度2

    Returns
    -------
    distance: float
        距离
    """
    try:
        lng1 = lng1.astype(float)
        lat1 = lat1.astype(float)
        lng2 = lng2.astype(float)
        lat2 = lat2.astype(float)
    except Exception:
        lng1 = float(lng1)
        lat1 = float(lat1)
        lng2 = float(lng2)
        lat2 = float(lat2)
    lng1, lat1, lng2, lat2 = map(lambda r: r * math.pi / 180, [lng1, lat1, lng2, lat2])
    d_lng = lng2 - lng1
    d_lat = lat2 - lat1
    a = math.sin(d_lat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(d_lng / 2) ** 2
    c = 2 * math.asin(a ** 0.5)
    r = 6371004  # 地球平均半径，单位为米
    return c * r


def calculate_mileage(coords):
    """计算里程数

    Parameters
    ----------
    coords: list
        坐标点列表

    Examples
    --------
    >>> calculate_mileage([[119.36110833333332,32.115410000000004]])
    >>> 0
    type: float
    
    >>> calculate_mileage([(119.36110833333332,32.115410000000004), (119.36119833333332,32.115410000000004)])
    >>> 8.475771005324928
    type: float
    
    Returns
    -------
    mileage: float
        通过坐标点计算的里程数
    """
    mileage = 0
    if len(coords) <= 1:
        return mileage
    for i in range(len(coords) - 1):
        mileage += get_flatter_distance(
            coord1=coords[i],
            coord2=coords[i + 1]
        )
    return mileage


def covert_from_arcgis(coord, unit=1):
    """来自argis直接复制的坐标格式化

    Parameters
    ----------
    coord: string
        argis软件复制的坐标
    unit: optional, default 1
        坐标单位, 1:默认单位格式为十进制 2:度分秒 3:十进制转度分秒

    Examples
    --------
    >>> covert_from_arcgis('119.3608938°东 32.1159870°北', 1)
    >>> [119.3608938, 32.115987]
    type: list

    >>> covert_from_arcgis('119°21'41"东 32°6'58"北', 2)
    >>> [119.36138888888888, 32.11611111111111]
    type: list

    >>> covert_from_arcgis('119.3608938°东 32.1159870°北', 3)
    >>> ["119°21'39.217679999998154", "32°6'57.55319999998903"]
    type: list

    Returns
    -------
    result: list
        以[lng, lat]格式返回格式化后的数据
    """
    result = []
    if unit == 1:
        return [float(xy.split('°')[0]) for xy in coord.split(' ')]
    elif unit == 2:
        temp = [xy.split('"')[0] for xy in coord.split(' ')]
        for item in temp:
            num = 0.0
            item = item.split('°')
            num += float(item[0])
            item = item[1].split('\'')
            num += float(item[0]) / 60
            num += float(item[1]) / 3600
            result.append(num)
        return result
    elif unit == 3:
        for item in [float(xy.split('°')[0]) for xy in coord.split(' ')]:
            print(item)
            degree = int(item)
            min = int((item - degree) * 60)
            second = (((item - degree) * 60) - min) * 60

            result.append('{0}°{1}\'{2}'.format(degree, min, second))
        return result
    else:
        raise Exception('The data origin must in [1, 2, 3]')


# if __name__ == '__main__':
#     # print(convert_to_baidu_single(119.3609491, 32.11607947))
#     print(convert_by_baidu([[119.2173359, 32.0693007], [119.2171111, 32.0692883]]))
#     # print(convert_to_tencent_single(119.3609491, 32.11607947))
#     # convert_to_tencent([[119.2169042, 32.069362], [119.2169042, 32.069362]])
#     # get_distance_by_baidu()
#     # get_flatter_distance((119.36110833333332,32.115410000000004), (119.36119833333332,32.115410000000004))
#     # [(119.35888,32.11242), (119.35898,32.11242)]
#     # print(calculate_mileage([(119.35888, 32.11242), (119.35898, 32.11242)]))
#     # print(get_distance(119.359038, 32.11255, 119.364167, 32.11883))
