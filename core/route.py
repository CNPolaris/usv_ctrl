"""
-------------------------------------------------
File Name: route
Description: 实现路径规划的核心线程
Author: TianXin
Date：2022-12-26
-------------------------------------------------
"""
from PySide6 import QtCore

from libs import area_to_grid, gen_grids_array, gps_to_grid
from route.demo import RRT


class RouteThread(QtCore.QThread):
    send_route_path = QtCore.Signal(list)
    check_lake_signal = QtCore.Signal(bool)

    def __init__(self):
        super(RouteThread, self).__init__()
        self.grid = None
        self.params = None
        self.grid_array = None
        self.accuracy = 5

    def run(self) -> None:
        print("开启路径规划线程")

    def gen_grid(self, bounds):
        self.grid, self.params = area_to_grid(location=bounds, accuracy=self.accuracy)
        self.grid_array = gen_grids_array(self.grid, self.params,
                                          lake_path="E:\\just\\海韵湖智能技术实验场\\data\\baidu_lake.shp",
                                          island_path="E:\\just\\海韵湖智能技术实验场\\data\\baidu_island.shp",
                                          show=False)
        print('生成地图矩阵完成')

    def set_start_end(self, start_end):
        print(start_end)
        obstacle_list = [(119.373225, 32.120244, 20), (119.372865, 32.118738, 10)]
        rrt = RRT(start=start_end[0], goal=start_end[1], grid=self.grid,
                  grid_array=self.grid_array,
                  params=self.params, obstacle_coords=obstacle_list)
        path = rrt.planning()
        self.send_route_path.emit(path)

    def set_accuracy(self, accuracy):
        self.accuracy = accuracy

    def check_in_lake(self, point):
        """检查起点或终点是否在水域中

        Parameters
        ----------
        point: list
            [lng, lat]: 坐标点

        Returns
        -------
        flag: bool, True: 在水域中, False: 在陆地上
        """
        row, col = gps_to_grid(point[0], point[1], self.params)[::-1]
        if self.grid_array[row][col] == 0:
            self.check_lake_signal.emit(True)
        else:
            self.check_lake_signal.emit(False)
