"""
矢量元素库
"""
import geopandas as gp
from shapely import geometry

from libs.convert import transform_degree, convert_to_baidu_single, convert_to_tencent_single
from libs.grids import area_to_grid


# GPS数据路径
# lake_original_path = 'E:\\just\\海韵湖智能技术实验场\\原始数据\\data\\环湖数据.txt'
# island_original_path = 'E:\\just\\海韵湖智能技术实验场\\原始数据\\data\\浮岛数据.txt'
lake_original_path = 'E:\\just\\海韵湖智能技术实验场\\原始数据\\processed\\lake.txt'
island_original_path = 'E:\\just\\海韵湖智能技术实验场\\原始数据\\processed\\baidu_island.txt'
# 是否保存
lake_save = True
island_save = True
grids_save = False
# shp存储路径
root_path = 'E:\\just\\海韵湖智能技术实验场\\data\\'
lake_save_path = '{0}baidu_lake.shp'.format(root_path)
island_save_path = '{0}baidu_island.shp'.format(root_path)
# grids_save_path = '{0}grids.shp'.format(root_path)
# 边界条件
x_max, x_min, y_min, y_max = float('-inf'), float('inf'), float('inf'), float('-inf')

# GPS度分秒格式
gps = False
# 百度地图
baidu = False
# 腾讯地图
tencent = False

# 环湖数据处理
lake_points = []
with open(lake_original_path) as f:
    lake_original_data = f.read()

for xy in lake_original_data.split(';'):
    y, _, x = xy.partition(',')
    # x = transform_degree(float(x.strip()))
    # y = transform_degree(float(y.strip()))
    x = float(x.strip())
    y = float(y.strip())
    if gps:
        x = transform_degree(x)
        y = transform_degree(y)
    # 第三方地图坐标转换
    if baidu:
        x, y = convert_to_baidu_single(x, y)[:2]
    if tencent:
        x, y = convert_to_tencent_single(x, y)[:2]
    # 边界
    if x > x_max:
        x_max = x
    if x < x_min:
        x_min = x
    if y > y_max:
        y_max = y
    if y < y_min:
        y_min = y
    lake_points.append(geometry.Point(x, y))
print(x_min, y_min, x_max,  y_max)
lake_poly = geometry.Polygon(lake_points)
lake = gp.GeoSeries(lake_poly)
print(lake.bounds)
# if lake_save:
#     lake.to_file(lake_save_path, driver='ESRI Shapefile', encoding='utf-8')

# 浮岛
# island_points = []
# with open(island_original_path) as f:
#     island_original_data = f.read()
# for xy in island_original_data.split(';'):
#     y, _, x = xy.partition(',')
#     # x = transform_degree(float(x.strip()))
#     # y = transform_degree(float(y.strip()))
#     x = float(x.strip())
#     y = float(y.strip())
#     if gps:
#         x = transform_degree(x)
#         y = transform_degree(y)
#     if baidu:
#         x, y = convert_to_baidu_single([x, y])[:2]
#     if tencent:
#         x, y = convert_to_tencent_single([x, y])[:2]
#     island_points.append(geometry.Point(x, y))
#
# island_poly = geometry.Polygon(island_points)
# island = gp.GeoSeries(island_poly)
# if island_save:
#     island.to_file(island_save_path, driver='ESRI Shapefile', encoding='utf-8')

# 栅格
# accuracy = 10
# grids, params = area_to_grid(location=lake_poly.bounds(), accuracy=accuracy)
# print('生成栅格参数', params)
# grids.set_crs('EPSG:4326', allow_override=True)
# if grids_save:
#     grids.to_file(grids_save_path, driver='ESRI Shapefile', encoding='utf-8')

print('执行结束')
