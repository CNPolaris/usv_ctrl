import os
import geopandas as gp
from shapely import geometry
import time
from convert import convert_by_baidu, convert_to_baidu_single

save_path = 'E:\\just\\海韵湖智能技术实验场\\原始数据\\processed'

lake_original_path = 'E:\\just\\海韵湖智能技术实验场\\原始数据\\processed\\lake.txt'
island_original_path = 'E:\\just\\海韵湖智能技术实验场\\原始数据\\processed\\island.txt'

root_path = 'E:\\just\\海韵湖智能技术实验场\\data\\'

bounds = [[119.359038, 32.11255], [119.364167, 32.11883]]
bounds_in_baidu = convert_by_baidu(bounds)

# result = []

# with open(lake_original_path) as f:
#     lake_data = f.read()
    
# for xy in lake_data.split(';'):
#     y, _, x = xy.partition(',')
#     x, y = convert_to_baidu_single(x, y)
#     result.append('{0},{1}'.format(y, x))
#     time.sleep(0.1)
    
# t = open(save_path + os.sep + '{0}.txt'.format('baidu_lake'), 'w')
# t.write(';'.join(result))
# t.close()

result = []
with open(island_original_path) as f:
    island_data = f.read()

for xy in island_data.split(';'):
    y, _, x = xy.partition(',')
    x, y = convert_to_baidu_single(x, y)
    result.append('{0},{1}'.format(y, x))
    time.sleep(0.1)
    
i = open(save_path + os.sep + '{0}.txt'.format('baidu_island'), 'w')
i.write(';'.join(result))
i.close()