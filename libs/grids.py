"""
栅格化工具库
"""
import geopandas as gp
import math
import pandas as pd
import numpy as np
from shapely import geometry
import os

from .convert import convert_by_baidu


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


def area_to_grid(location, accuracy=10, method='rect', params='auto', form='line'):
    """在范围内生成栅格

    Parameters
    ----------
    location: bounds(List) or shape(GeoDataFrame)
        栅格的边界 如果是bounds, 则内容是[lng1, lat1, lng2, lat2] (WGS84坐标系) 其中lng1,lat1是左下角坐标,lng2, lat2是右上角坐标
        如果是要素, 那么必须是GeoDataFrame
    accuracy: number, default 10
        栅格大小 米
    method: str, default rect
        栅格形状:
            'rect': 方形
    params: list or dict, default auto
        栅格参数
    form: str, default line
        如果是line, 生成线性元素; 如果是poly, 生成面元素

    Returns
    -------
       grid : GeoDataFrame
            栅格矢量元素
       params : list or dict
            栅格参数
    """
    if (type(location) == list) | (type(location) == tuple):
        shape = ''
        bounds = location
    elif type(location) == gp.GeoDataFrame:
        shape = location
        bounds = shape.unary_union.bounds
    else:
        raise Exception('Location should be bounds or shape')

    lng1, lat1, lng2, lat2 = bounds
    if (lng1 > lng2) | (lat1 > lat2) | (abs(lat1) > 90) | (abs(lng1) > 180) | (abs(lat2) > 90) | (abs(lng2) > 180):
        raise Exception('经纬度大小超出')

    lat_start = min(lat1, lat2)
    lng_start = min(lng1, lng2)
    delta_lng = accuracy * 360 / (2 * math.pi * 6371004 * math.cos((lat1 + lat2) * math.pi / 360))
    delta_lat = accuracy * 360 / (2 * math.pi * 6371004)
    if params == 'auto':
        params = {
            'slng': lng_start,
            'slat': lat_start,
            'delta_lng': delta_lng,
            'delta_lat': delta_lat,
            'theta': 0,
            'method': method,
            'grid_size': accuracy,
            'form': form
        }
    else:
        params = convert_params(params)
        method = params['method']
    if method == 'rect':
        temp_points = pd.DataFrame(np.array(
            np.meshgrid(
                np.arange(bounds[0],
                          bounds[2],
                          delta_lng / 2),
                np.arange(bounds[1],
                          bounds[3],
                          delta_lat)
            )).reshape(2, -1).T, columns=['lng', 'lat'])
        temp_points['lng_col'], temp_points['lat_col'] = gps_to_grid(temp_points['lng'], temp_points['lat'], params)
        temp_points = temp_points[['lng_col', 'lat_col']].drop_duplicates()
        temp_points['geometry'] = grid_to_polygon([temp_points['lng_col'], temp_points['lat_col']], params)
        temp_points = gp.GeoDataFrame(temp_points)

    data = temp_points
    params['grid_size'] = accuracy
    if type(shape) != gp.GeoDataFrame:
        grid = gp.GeoDataFrame(data)
        params['rows_num'] = grid.lat_col.nunique()
        params['columns_num'] = grid.lng_col.nunique()
        return grid, params
    else:
        data.crs = shape.crs
        data = data[data.intersects(shape.unary_union)]
        grid = gp.GeoDataFrame(data)
        params['rows_num'] = grid.lat_col.nunique()
        params['columns_num'] = grid.lng_col.nunique()
        return grid, params


def area_to_grid_2(location, accuracy=10, form='line'):
    """在范围内生成栅格

    Parameters
    ----------
    location: bounds(List) or shape(GeoDataFrame)
        栅格的边界 如果是bounds, 则内容是[lng1, lat1, lng2, lat2] (WGS84坐标系) 其中lng1,lat1是左下角坐标,lng2, lat2是右上角坐标
        如果是要素, 那么必须是GeoDataFrame
    accuracy: number, default 10
        栅格大小 米
    form: str, default line
        形状

    Returns
    -------
       grid : GeoDataFrame
            栅格矢量元素
    """
    params = dict()
    if (type(location) == list) | (type(location) == tuple):
        bounds = location

    lng1, lat1, lng2, lat2 = bounds
    lat_start = min(lat1, lat2)
    lng_start = min(lng1, lng2)
    delta_lng = accuracy * 360 / (2 * math.pi * 6371004 * math.cos((lat1 + lat2) * math.pi / 360))
    delta_lat = accuracy * 360 / (2 * math.pi * 6371004)
    grid_rows_num = int(math.ceil((lat2 - lat1) / float(delta_lat)))
    grid_columns_num = int(math.ceil((lng2 - lng1) / float(delta_lng)))
    grid_lines = []
    for r in range(grid_rows_num):
        for c in range(grid_columns_num):
            grid_4coords = []
            # 左上角
            x_lt = lng_start + c * delta_lng
            y_lt = lat2 - r * delta_lat
            # 右上角
            x_rt = x_lt + delta_lng
            y_rt = y_lt
            # 左下角
            x_lb = x_lt
            y_lb = y_lt - delta_lat
            # 右下角
            x_rb = x_rt
            y_rb = y_lb
            # 两个三角形拼接一个栅格
            grid_4coords.append(geometry.Point(x_lt, y_lt))
            grid_4coords.append(geometry.Point(x_rt, y_rt))
            grid_4coords.append(geometry.Point(x_rb, y_rb))
            grid_4coords.append(geometry.Point(x_lb, y_lb))
            grid_4coords.append(geometry.Point(x_lt, y_lt))
            # 创建一个网格
            grid_lines.append(geometry.LineString(grid_4coords))
    grid = gp.GeoSeries(grid_lines, crs='EPSG:4326')
    params['rows_num'] = grid_rows_num
    params['columns_num'] = grid_columns_num
    return grid, params


def convert_params(params):
    """参数转换

    Parameters
    ----------
    params: list or dict or tuple
        栅格参数

    Returns
    -------
    params: dict
        栅格参数
    """
    if (type(params) == list) | (type(params) == tuple):
        if len(params) == 4:
            lng_start, lat_start, delta_lng, delta_lat = params
            theta = 0
            method = 'rect'
        elif len(params) == 5:
            lng_start, lat_start, delta_lng, delta_lat, theta = params
            method = 'rect'
        elif len(params) == 6:
            lng_start, lat_start, delta_lng, delta_lat, theta, method = params
        dict_params = dict()
        dict_params['slng'] = lng_start
        dict_params['slat'] = lat_start
        dict_params['delta_lng'] = delta_lng
        dict_params['delta_lat'] = delta_lat
        dict_params['theta'] = theta
        dict_params['method'] = method
    else:
        dict_params = params
        if 'theta' not in dict_params:
            dict_params['theta'] = 0
        if 'method' not in dict_params:
            dict_params['method'] = 'rect'
    if dict_params['method'] not in ['rect', 'tri', 'hexa']:
        raise ValueError('Method should be `rect`,`tri` or `hexa`')
    return dict_params


def gps_to_grid(lng, lat, params):
    """GPS数据对应的栅格编号
        从第经度、纬度起点开始进行编号，参照平面二维直角坐标系的建立

    Parameters
    ----------
    lng: Series
        经度列
    lat: Series
        纬度列
    params: list or dict
        参数

    Returns
    -------
    [lng_col, lat_col]: list
        方形栅格输出: 栅格编号两列[x, y]
    [array([ 0, 48]), array([ 0, 69])]: list
        分别为x列, y列
    """
    params = convert_params(params)
    method = params['method']

    if method == 'rect':
        lng_col, lat_col = gps_to_grids_rect(lng, lat, params)
        return [lng_col, lat_col]


def gps_to_grids_rect(lng, lat, params, from_origin=True):
    """在栅格中找到对应GPS数据的栅格编号

    Parameters
    ----------
    lng: Series
        经度列
    lat: Series
        纬度列
    params: list or dict
        栅格参数
    from_origin: bool,default False
        if True: lng_start,lat_start 是第一个栅格的左下角坐标点
        if False: lng_start, lat_start 是第一个栅格的中心坐标点

    Returns
    -------
    [lng_col, lat_col]: list
    """
    params = convert_params(params)
    lng_start = params['slng']
    lat_start = params['slat']
    delta_lng = params['delta_lng']
    delta_lat = params['delta_lat']
    theta = params['theta']

    lng = pd.Series(lng)
    lat = pd.Series(lat)
    cos_theta = np.cos(theta * np.pi / 180)
    sin_theta = np.sin(theta * np.pi / 180)
    R = np.array([[cos_theta * delta_lng, -sin_theta * delta_lat],
                  [sin_theta * delta_lng, cos_theta * delta_lat]])
    coords = np.array([lng, lat]).T
    if from_origin:
        coords = coords - (np.array([lng_start, lat_start]))
    else:
        coords = coords - (np.array([lng_start, lat_start]) - R[0, :] / 2 -
                           R[1, :] / 2)
    res = np.floor(np.dot(coords, np.linalg.inv(R)))
    lng_col = res[:, 0].astype(int)
    lat_col = res[:, 1].astype(int)
    if len(lng_col) == 1:
        lng_col = lng_col[0]
        lat_col = lat_col[0]
    return lng_col, lat_col


def grid_to_polygon(grid_id, params):
    """栅格编号生成栅格的地理信息列
        输入数据的栅格编号与栅格参数，输入对应的地理信息列

    Parameters
    ----------
    grid_id: list
        方形栅格:
        [lng_col, lat_col]: list
            栅格编号两列
    params: list or dict
        栅格参数
    Returns
    -------
    geometry: Series
        栅格的矢量图形列
    """
    params = convert_params(params)
    method = params['method']

    if method == 'rect':
        lng_col, lat_col = grid_id
        return grid_to_polygon_rect(lng_col, lat_col, params)


def grid_to_polygon_rect(lng_col, lat_col, params):
    """基于栅格编号生成指定形状的矢量图形列

    Parameters
    ----------
    lng_col: Series
        经度列
    lat_col: Series
        纬度列
    params: list or dict
        栅格参数

    Returns
    -------
    geometry: Series
        矢量图形列
    """
    params = convert_params(params)
    lng_start = params['slng']
    lat_start = params['slat']
    delta_lng = params['delta_lng']
    delta_lat = params['delta_lat']
    theta = params['theta']
    lng_col = pd.Series(lng_col)
    lat_col = pd.Series(lat_col)
    cos_theta = np.cos(theta * np.pi / 180)
    sin_theta = np.sin(theta * np.pi / 180)
    R = np.array([[cos_theta * delta_lng, -sin_theta * delta_lat],
                  [sin_theta * delta_lng, cos_theta * delta_lat]])
    res_a = np.array([lng_col.values - 0.5, lat_col.values - 0.5]).T
    res_b = np.array([lng_col.values + 0.5, lat_col.values - 0.5]).T
    res_c = np.array([lng_col.values + 0.5, lat_col.values + 0.5]).T
    res_d = np.array([lng_col.values - 0.5, lat_col.values + 0.5]).T
    deathblow_a = np.dot(res_a, R) + np.array([lng_start, lat_start])
    deathblow_b = np.dot(res_b, R) + np.array([lng_start, lat_start])
    deathblow_c = np.dot(res_c, R) + np.array([lng_start, lat_start])
    deathblow_d = np.dot(res_d, R) + np.array([lng_start, lat_start])
    a = deathblow_a
    b = deathblow_b
    c = deathblow_c
    d = deathblow_d
    if params['form'] == 'line':
        return [geometry.LineString([a[i], b[i], c[i], d[i], a[i]]) for i in range(len(a))]
    elif params['form'] == 'poly':
        return [geometry.Polygon([a[i], b[i], c[i], d[i], a[i]]) for i in range(len(a))]


def gps_index_in_grids(grid, lng, lat):
    """坐标点在栅格中的位置
    输入栅格矢量列, 经度，纬度(十进制度数), 返回坐标点出现的位置列

    Parameters
    ----------
    grid: list, Series of geometry
        矢量数据下的栅格矢量列
    lng: float
        经度
    lat: float
        纬度

    Returns
    -------
    index: list
        坐标点出现的位置
    """

    try:
        lng = lng.astype(lng)
        lat = lat.astype(lat)
    except Exception:
        lng = float(lng)
        lat = float(lat)
    if type(grid) == gp.GeoDataFrame:
        grid = grid['geometry']
    point = geometry.Point(lng, lat)
    for i in grid:
        if i.contains(point):
            print(i)


def get_bounds_from_original_data(path, processed=True):
    """从原始数据中获取研究区域边界

    Parameters
    ----------
    path: str
        原始数据路径
    processed: bool
        是否已经处理成十进制度数, If True 不调用transform_degree进行转换 不然调用

    Returns
    -------
    bounds: list
        研究区域边界
            [lng1,lat1,lng2,lat2]
    """
    if not os.path.exists(path):
        raise Exception('File not exits')
    with open(path) as f:
        data = f.read()
    x_max, x_min, y_min, y_max = float('-inf'), float('inf'), float('inf'), float('-inf')
    for xy in data.split(';'):
        y, _, x = xy.partition(',')
        if not processed:
            x = transform_degree(float(x.strip()))
            y = transform_degree(float(y.strip()))
        x = float(x.strip())
        y = float(y.strip())
        if x > x_max:
            x_max = x
        if x < x_min:
            x_min = x
        if y > y_max:
            y_max = y
        if y < y_min:
            y_min = y
    return [x_min, y_min, x_max, y_max]


def get_bounds_from_shp(path):
    """从shapefile矢量文件中获取研究区域边界

    Parameters
    ----------
    path: str
        矢量文件路径

    Returns
    -------
    bounds: list
        研究区域边界
            [lng1, lat1, lng2, lat2]
    """
    if not os.path.exists(path):
        raise Exception('Shapefile not exists')
    bounds = gp.read_file(path).bounds.iloc[0]

    bounds = [item for item in bounds]
    return bounds


def get_bounds_from_file(path, is_shp=False):
    """从文件中读取研究区域边界边界

    Parameters
    ----------
    path: str
        文件路径
    is_shp: bool
        是否为shapefile文件, 默认为False
        if True, 调用get_bounds_from_shp()
        if False, 调用get_bounds_from_original_data()

    Returns
    -------
    bounds:list
        研究区域边界
    """
    if is_shp:
        return get_bounds_from_shp(path)
    else:
        return get_bounds_from_original_data(path)


def check_in_lake(lake_df, island_df, shape):
    """检查矢量元素是否在水域中
    输入水域,浮岛shp文件, 和要检查的矢量元素

    Parameters
    ----------
    lake_df: Series or GeoDataFrame
        水域shp文件路径
    island_df: Series or GeoDataFrame
        浮岛shp文件路径
    shape: GeoDataFrame or Shape
        矢量元素

    Returns
    -------
    in_lake: bool
        是否在水域中, True:在水域中 False:陆地或浮岛
    """
    if island_df.iloc[0]['geometry'].intersects(shape):
        return False
    else:
        return lake_df.iloc[0]['geometry'].intersects(shape)


def gen_grids_array(grid, params, lake_path=None, island_path=None, show=False):
    """生成栅格矩阵 输入生成的栅格，栅格参数，水域shp文件路径，浮岛shp文件路径

    Parameters
    ----------
    grid: GeoSeries,GeoDataFrame or list
        栅格矢量数据
    params: list or dict
        栅格参数
    lake_path: str
        环湖数据路径
    island_path: str
        浮岛数据路径
    show: bool
        是否打印生成的矩阵, If True 打印生成的矩阵

    Returns
    -------
    grid_array: list
        栅格化矩阵
            0表示水域, 1表示陆地或障碍物
    """
    if lake_path is not None:
        if not os.path.exists(lake_path):
            raise Exception('Lake shapefile not exist, Please create lake shapefile')
        lake_df = gp.read_file(lake_path)
    else:
        lake_df = None
    if island_path is not None:
        if not os.path.exists(island_path):
            raise Exception('Island shapefile not exist')
        island_df = gp.read_file(island_path)
    else:
        island_df = None
    params = convert_params(params)
    rows_num = params['rows_num']
    columns_num = params['columns_num']

    if type(grid) == gp.GeoDataFrame:
        grid = grid['geometry'].to_list()
    if type(grid) == gp.GeoSeries:
        grid = grid.to_list()
    # 生成矩阵
    grid_array = []
    for r in range(rows_num)[::-1]:
        row_array = []
        for c in range(columns_num):
            index = (rows_num - r - 1) * columns_num + c
            if lake_df is not None and island_df is not None:
                if check_in_lake(lake_df, island_df, grid[index]):
                    row_array.append(0)
                else:
                    row_array.append(1)
            else:
                row_array.append(0)
        grid_array.append(row_array)
    if show:
        print_grid_array(grid_array, rows_num, columns_num)
    return grid_array


def grid_to_centre(gridid, params):
    '''
    栅格编号对应栅格中心点经纬度

    输入数据的栅格编号与栅格参数，输出对应的栅格中心点
    Parameters
    -------
    gridid : list
        方形栅格:
        [LONCOL,LATCOL] : list
            栅格编号两列
        三角形、六边形栅格:
        [loncol_1,loncol_2,loncol_3] : list
            栅格编号三列
    params : list or dict
        栅格参数
    Returns
    -------
    HBLON : Series
        栅格中心点经度列
    HBLAT : Series
        栅格中心点纬度列
    '''
    params = convert_params(params)
    method = params['method']
    if method == 'rect':
        lngcol, latcol = gridid
        lngcol = pd.Series(lngcol, name='lngcol')
        latcol = pd.Series(latcol, name='latcol')
        return grid_to_centre_rect(lngcol, latcol, params, from_origin=False)


def grid_to_centre_rect(lng_col, lat_col, params, from_origin=False):
    '''
    The center location of the grid for rect grids. The input is the
    grid ID and parameters, the output is the grid center location.
    Parameters
    -------
    LONCOL : Series
        The index of the grid longitude. The two columns LONCOL and
        LATCOL together can specify a grid.
    LATCOL : Series
        The index of the grid latitude. The two columns LONCOL and
        LATCOL together can specify a grid.
    params : List
        Gridding parameters (lng_start, lat_start, delta_lng, delta_lat) or
        (lng_start, lat_start, delta_lng, delta_lat, theta).
        lng_start and lat_start are the lower-left coordinates;
        delta_lng, delta_lat are the length and width of a single grid;
        theta is the angle of the grid, it will be 0 if not given.
        When Gridding parameters is given, accuracy will not be used.
    from_origin : bool
        If True, lng_start and lat_start are the lower left of the first
        grid.
        If False, lng_start and lat_start are the center of the first
        grid.
    Returns
    -------
    HBLON : Series
        The longitude of the grid center
    HBLAT : Series
        The latitude of the grid center
    '''
    params = convert_params(params)
    lng_start = params['slng']
    lat_start = params['slat']
    delta_lng = params['delta_lng']
    delta_lat = params['delta_lat']
    theta = params['theta']

    lng_col = pd.Series(lng_col)
    lat_col = pd.Series(lat_col)
    costheta = np.cos(theta * np.pi / 180)
    sintheta = np.sin(theta * np.pi / 180)
    R = np.array([[costheta * delta_lng, -sintheta * delta_lat],
                  [sintheta * delta_lng, costheta * delta_lat]])
    if from_origin:
        hb_lng_hb_lat = np.dot(np.array([lng_col.values, lat_col.values]).T,
                               R) + np.array([lng_start, lat_start]) - (
                                R[0, :] / 2 + R[1, :] / 2)
    else:
        hb_lng_hb_lat = np.dot(np.array([lng_col.values, lat_col.values]).T,
                               R) + np.array([lng_start, lat_start])
    hb_lng = hb_lng_hb_lat[:, 0]
    hb_lat = hb_lng_hb_lat[:, 1]
    if len(hb_lng) == 1:
        hb_lng = hb_lng[0]
        hb_lat = hb_lat[0]
    return hb_lng, hb_lat


def print_grid_array(grid_array, rows_num, columns_num):
    """打印栅格矩阵

    Parameters
    ----------
    grid_array: list
        栅格矩阵
    rows_num: number
        行数
    columns_num: number
        列数

    Returns
    -------

    """
    print('\n')
    for i in range(rows_num)[::-1]:
        t = ''
        for j in range(columns_num):
            t += ' ' + str(grid_array[i][j])
        print(t)


def grid_to_params(grid):
    """
    从栅格数据重新生成栅格参数

    Parameters
    ----------
    grid: GeoDataFrame
        方形栅格的矢量数据

    Returns
    -------
    params: list or dict
        栅格参数 slng: 起始经度, slat: 起始纬度, delta_lng: 单个栅格经度,
        delta_lat: 单个栅格纬度, theta: 偏向度, method: 栅格形状, rows_num: 行数, columns_num: 列数
    """
    grid_coord = np.array(grid['geometry'].iloc[0].coords)
    lng_col = grid['lng_col'].iloc[0]
    lat_col = grid['lat_col'].iloc[0]
    hb_lng = grid['geometry'].iloc[0].centroid.x
    hb_lat = grid['geometry'].iloc[0].centroid.y
    grid_coord = grid_coord - grid_coord[0]
    x = grid_coord[1]
    y = grid_coord[3]
    R = np.array([x, y])
    lng_tart, lat_start = np.array([hb_lng, hb_lat
                                    ]) - R[0, :] * lng_col - R[1, :] * lat_col
    delta_lng = (x[0] ** 2 + y[0] ** 2).sum() ** 0.5
    delta_lat = (x[1] ** 2 + y[1] ** 2).sum() ** 0.5
    theta = np.arccos(x[0] / delta_lng) * 180 / np.pi
    if np.allclose(theta, 0):
        params = [lng_tart, lat_start, delta_lng, delta_lat]
    else:
        params = [lng_tart, lat_start, delta_lng, delta_lat, theta]
    params = convert_params(params)
    params['rows_num'] = grid['lat_col'].nunique()
    params['columns_num'] = grid['lng_col'].nunique()
    return params


def insert_obstacle_into_grids(grid, grid_array, params, obstacles, show=False):
    """在栅格矩阵中插入障碍物

    Parameters
    ----------
    grid: GeoDataFrame or GeoSeries or list
        栅格矢量元素列表
    grid_array: list
        栅格矩阵
    params: list or dict
        栅格参数
    obstacles: list
        障碍物列表
        [lng, lat, size]:中心坐标与半径
    show: bool, default False
        是否打印

    Returns
    -------
    grid_array: list
        栅格矩阵
    """
    if type(grid) == gp.GeoDataFrame:
        grid = grid['geometry'].to_list()
    if type(grid) == gp.GeoSeries:
        grid = grid.to_list()
    params = convert_params(params)
    rows_num = params['rows_num']
    columns_num = params['columns_num']
    for (ox, oy, size) in obstacles:
        distance = size * 360 / (2 * math.pi * 6371004 * math.cos(oy))
        obstacle = geometry.Point(ox, oy).buffer(distance)
        for r in range(rows_num):
            for c in range(columns_num):
                index = r * columns_num + c
                if obstacle.intersects(grid[index]):
                    grid_array[r][c] = 1
    if show:
        print_grid_array(grid_array, rows_num, columns_num)
    return grid_array


def remove_obstacle_from_grids(grid, grid_array, params, obstacles, show=False):
    """从栅格矩阵中移除障碍物

    Parameters
    ----------
    grid: GeoDataFrame or GeoSeries or list
        栅格矢量元素列表
    grid_array: list
        栅格矩阵
    params: list or dict
        栅格参数
    obstacles: list
        障碍物列表
        [lng, lat, size]:中心坐标与半径
    show: bool, default False
        是否打印

    Returns
    -------
    grid_array: list
        栅格矩阵
    """
    if type(grid) == gp.GeoDataFrame:
        grid = grid['geometry'].to_list()
    if type(grid) == gp.GeoSeries:
        grid = grid.to_list()
    params = convert_params(params)
    rows_num = params['rows_num']
    columns_num = params['columns_num']
    for (ox, oy, size) in obstacles:
        distance = size * 360 / (2 * math.pi * 6371004 * math.cos(oy))
        obstacle = geometry.Point(ox, oy).buffer(distance)
        for r in range(rows_num):
            for c in range(columns_num):
                index = r * columns_num + c
                if obstacle.intersects(grid[index]) and grid_array[r][c] == 1:
                    grid_array[r][c] = 0
    if show:
        print_grid_array(grid_array, rows_num, columns_num)
    return grid_array


def get_grid_by_index(index, grid, params):
    """通过在栅格矩阵的索引获取对应栅格的矢量信息

    Parameters
    ----------
    index: list or tuple or int
        实际位置，而不是在矩阵内的物理位置
    grid: GeoDataFrame or GeoSeries or list
        栅格矢量数据列
    params: list or dict
        栅格参数

    Returns
    -------
    shape: GeoDataFrame or geometry.LineString
        索引对应的栅格矢量信息
    """
    params = convert_params(params)
    rows_num = params['rows_num']
    columns_num = params['columns_num']

    if ((type(index) == list) | (type(index) == tuple)) and \
            (0 <= index[0] < rows_num and 0 <= index[1] < columns_num):
        index = (index[0] - 1) * columns_num + index[1] - 1
    elif index > rows_num * columns_num:
        raise Exception('The grid index must in range(0, {})'.format(rows_num * columns_num))

    if type(grid) == gp.GeoDataFrame:
        grid_list = grid['geometry'].to_list()
    elif type(grid) == gp.GeoSeries:
        grid_list = grid.to_list()
    elif type(grid) == list:
        grid_list = grid
    else:
        raise Exception('The grid type must is GeoDataFrame or GeoSeries or list')

    return grid_list[index - 1]


def get_near_grid_info(grid, params, grid_array, index):
    """get_near_grid_info 获取周围栅格的信息
        根据在栅格矩阵的索引位置或者栅格矢量列中的索引获取周围临近栅格信息

    Parameters
    ----------
    grid : GeoDataFrame or GeoSeries or List
        栅格矢量列
    params : list or dict
        栅格参数
    grid_array : list
        栅格矩阵
    index : int or list or tuple
        相对位置

    Returns
    -------
    result: dict
        周围栅格的信息，包括边界坐标点，水域或陆地类型标识
            1:陆地 2:水域
    """
    params = convert_params(params)
    rows_num = params['rows_num']
    columns_num = params['columns_num']

    if type(grid) == gp.GeoDataFrame:
        grid_list = grid['geometry'].to_list()
    elif type(grid) == gp.GeoSeries:
        grid_list = grid.to_list()

    if type(index) == int:
        if not 0 < index <= rows_num * columns_num:
            raise Exception(
                'The index must in range(0, {0}), but the index is {1}'.format(rows_num * columns_num, index))
        c = index % columns_num
        r = (index - c) // columns_num + 1
        index = (r - 1) * columns_num + c - 1

    if (type(index) == list) | (type(index) == tuple):
        r, c = index
        index = (r - 1) * columns_num + c - 1
        if not 0 < r <= rows_num and 0 < c <= columns_num:
            raise Exception('For the index r and c must in range(0, {0}) or range(0, {1}),' +
                            'but the r is {2},the c is {3}'.format(rows_num, columns_num, r, c))

    result = dict()
    index_grid, index_array = grid_list[index], grid_array[r - 1][c - 1]
    result['index_grid'] = index_grid.bounds
    result['index_type'] = index_array

    if r + 1 <= rows_num:
        top_index = r * columns_num + c - 1
        result['top_grid'] = grid_list[top_index].bounds
        result['top_type'] = grid_array[r][c - 1]
    if c + 1 <= columns_num:
        left_index = (r - 1) * columns_num + c
        result['right_grid'] = grid_list[left_index].bounds
        result['right_type'] = grid_array[r - 1][c]
    if r - 1 > 0:
        bottom_index = (r - 2) * columns_num + c - 1
        result['bottom_grid'] = grid_list[bottom_index].bounds
        result['bottom_type'] = grid_array[r - 2][c - 1]
    if c - 1 > 0:
        right_index = (r - 1) * columns_num + c - 2
        result['left_grid'] = grid_list[right_index].bounds
        result['left_type'] = grid_array[r - 1][c - 2]
    return result


def gen_path_coord_from_grid(grid, grid_path, params):
    """通过栅格矩阵生成的路径提取出对应矢量栅格中心

    Parameters
    ----------
    grid: GeoDataFrame or GeoSeries or list
        栅格矢量元素
    grid_path: list
        栅格矩阵规划出的路径
        [row, col]: [行号, 列号]
    params: list or dict
        栅格参数

    Returns
    -------
    result: list
        矢量路径中的栅格中心
    """
    if type(grid) == gp.GeoDataFrame:
        grid_list = grid['geometry'].to_list()
    elif type(grid) == gp.GeoSeries:
        grid_list = grid.to_list()
    else:
        raise Exception('The grid type must is GeoDataFrame or GeoSeries')

    params = convert_params(params)
    columns_num = params['columns_num']
    result = []

    for xy in grid_path:
        index = (xy[0] - 1) * columns_num + xy[1] - 1
        result.append([grid_list[index].centroid.x, grid_list[index].centroid.y])
    return result


def gen_grid_to_baidu_polygon(grid=None, bounds=None, accuracy=10, processed=True, f=1):
    """gen_grid_to_baidu_polygon 将栅格矢量数据转换成百度地图栅格图层的数据格式
        grid 和 bounds不能同时为空
    
    Parameters
    ----------
    grid : GeoDataFrame or GeoSerial or list, optional
        栅格矢量数据列, by default None
    bounds : list or tuple, optional
        研究区域边界点, by default None
        可以是非百度地图标准坐标
    accuracy : int, optional
        栅格精确度, by default 10
    processed : bool, optional
        是否为百度地图标准坐标, 如果不是, 使用转换接口进行处理, by default True
    f : int, optional
        坐标原始格式, by default 1

    Returns
    -------
    grid_list: list
        转换后的适配百度地图的栅格数据
    params: list
        栅格化参数
        
    Raises
    ------
    Exception
        grid和bounds不能同时为空
    Exception
        grid的数据格式不正确
    """
    if grid is None and bounds is None:
        raise Exception("Grid or bounds must have one of them!!!\n" +
                        "If grid is not None,convert directly\n",
                        "If bounds is not None, convert by area_to_grid first\n")
    if grid is None and bounds is not None:
        lng1, lat1, lng2, lat2 = bounds
        if not processed:
            baidu_coords = convert_by_baidu([[lng1, lat1], [lng2, lat2]], f)
            lng1, lat1 = baidu_coords[0]
            lng2, lat2 = baidu_coords[1]
        grid, params = area_to_grid([lng1, lat1, lng2, lat2], accuracy=accuracy)

    grid_list = []
    if type(grid) == gp.GeoDataFrame:
        grid = grid['geometry'].to_list()
    elif type(grid) == gp.GeoSeries:
        grid = grid.to_list()
    elif type(grid) == list:
        grid = grid
    else:
        raise Exception('The type of grid must in GeoDataFrame or GeoSeries or list of shape\n')
    for i in range(len(grid)):
        lng1, lat1, lng2, lat2 = grid[i].bounds
        grid_list.append({
            'geometry': {
                'type': "Polygon",
                'coordinates': [
                    [
                        [lng1, lat1],
                        [lng2, lat1],
                        [lng2, lat2],
                        [lng1, lat2]
                    ]
                ]
            }
        })
    return grid_list, params


# TODO:这样的计算方法是有问题的
def get_index_in_array(points, params):
    result = []
    params = convert_params(params)
    s_lng = params['slng']
    s_lat = params['slat']
    delta_lng = params['delta_lng']
    delta_lat = params['delta_lat']
    for point in points:
        if (point['lng'] - s_lng) % delta_lng == 0:
            c = int((point['lng'] - s_lng) // delta_lng)
        else:
            c = int((point['lng'] - s_lng) // delta_lng) + 1
        if (point['lat'] - s_lat) % delta_lat == 0:
            r = int((point['lat'] - s_lat) // delta_lat)
        else:
            r = int((point['lat'] - s_lat) // delta_lat) + 1
        result.append([r, c])
    return result
