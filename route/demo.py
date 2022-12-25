"""
-------------------------------------------------
File Name: demo
Description:
Author: TianXin
Date：2022-12-15
-------------------------------------------------
"""
import numpy as np
import math
import matplotlib.pyplot as plt
import random

from libs.grids import *
from utils.logger import logger


class Node(object):
    def __init__(self, row, col) -> None:
        self.row = row
        self.col = col
        self.parent = None


class RRT(object):

    def __init__(self, start, goal, grid, grid_array, params, obstacle_coords) -> None:
        self.start = start
        self.goal = goal
        self.obstacle_coords = obstacle_coords
        self.start_node = None
        self.goal_node = None
        self.grids = grid
        self.params = params
        self.grid_array = grid_array
        self.row_num = 0
        self.col_num = 0

        self.node_list = []

        self.gen_grid()

    def gen_grid(self) -> None:
        """数据预处理以及矩阵生成

        Returns
        -------

        """
        self.start = gps_to_grid(self.start[0], self.start[1], self.params)[::-1]
        self.goal = gps_to_grid(self.goal[0], self.goal[1], self.params)[::-1]
        logger.info(f'起点位置: {self.start[0]}行, {self.start[1]}列')
        logger.info(f'终点位置: {self.goal[0]}行, {self.goal[1]}列')
        logger.info(self.params)
        self.start_node = Node(self.start[0], self.start[1])
        self.goal_node = Node(self.goal[0], self.goal[1])
        self.node_list.append(self.start_node)

        self.row_num = self.params["rows_num"]
        self.col_num = self.params["columns_num"]

        self.grid_array = insert_obstacle_into_grids(self.grids, self.grid_array, self.params, self.obstacle_coords)

    def get_sample_point(self):
        """研究区域内生成随机点

        Returns
        -------
        node:
            [row, col]: 随机点所在的行列号
        """
        while True:
            # 横坐标
            row = random.randint(min(self.start_node.row, self.goal_node.row + 1), max(self.start_node.row,
                                                                                       self.goal_node.row + 1))
            # 纵坐标
            col = random.randint(min(self.start_node.col, self.goal_node.col + 1), max(self.start_node.col,
                                                                                       self.goal_node.col + 1))
            if self.grid_array[row][col] == 0:
                break
        return [row, col]

    def get_near_list_index(self, rnd):
        """获取距离随机点最近的节点作为父节点

        Parameters
        ----------
        rnd: list
            [row, col]: 随机点的行列号

        Returns
        -------
        min_index: int
            最近节点的索引
        """
        d_list = []
        for i in range(len(self.node_list)):
            node = self.node_list[i]
            d_list.append(np.linalg.norm(np.array([node.row, node.col]) - np.array([rnd[0], rnd[1]])))
        min_index = d_list.index(min(d_list))
        return min_index

    def get_child_node(self, parent_node, sample_point):
        """生成子节点
            选取父节点周围的16个节点作为备选节点， 根据随机点的角度选择子节点

        Parameters
        ----------
        parent_node: Node
            父节点
        sample_point: list
            随机节点

        Returns
        -------
        child_node: Node
            生成的子节点
        """
        child_node_set = np.array([[parent_node.row + 2, parent_node.col],
                                   [parent_node.row + 2, parent_node.col + 1],
                                   [parent_node.row + 2, parent_node.col + 2],
                                   [parent_node.row + 1, parent_node.col + 2],
                                   [parent_node.row, parent_node.col + 2],
                                   [parent_node.row - 1, parent_node.col + 2],
                                   [parent_node.row - 2, parent_node.col + 2],
                                   [parent_node.row - 2, parent_node.col + 1],
                                   [parent_node.row - 2, parent_node.col],
                                   [parent_node.row - 2, parent_node.col - 1],
                                   [parent_node.row - 2, parent_node.col - 2],
                                   [parent_node.row - 1, parent_node.col - 2],
                                   [parent_node.row, parent_node.col - 2],
                                   [parent_node.row + 1, parent_node.col - 2],
                                   [parent_node.row + 2, parent_node.col - 2],
                                   [parent_node.row + 2, parent_node.col - 1]])
        theta_set = np.linspace(0, 2 * np.pi, 16)
        theta = math.atan2((sample_point[1] - parent_node.col), (sample_point[0] - parent_node.row))
        if theta < 0:
            theta += 2 * np.pi
        for i in range(16):
            if theta_set[i] <= theta < theta_set[i + 1]:
                child_node_idx = i
                break
        child_node = child_node_set[child_node_idx, :]
        return child_node

    def judge_obs(self, parent_node, child_node):
        # TODO:避障需要进一步细化
        flag = 0
        if self.grid_array[child_node[0]][child_node[1]] == 1:
            flag = 1
            return flag
        row_min = min(child_node[0], parent_node.row)
        row_max = max(child_node[0], parent_node.row)
        col_min = min(child_node[1], parent_node.col)
        col_max = max(child_node[1], parent_node.col)

        for i in range(row_min, row_max + 1):
            for j in range(col_min, col_max + 1):
                p = np.array([j, i])
                vec1 = np.array([parent_node.row, parent_node.col]) - p
                vec2 = np.array([child_node[0], child_node[1]]) - p
                distance = np.abs(np.cross(vec1, vec2)) / np.linalg.norm(
                    np.array([parent_node.row, parent_node.col]) - np.array([child_node[0], child_node[1]]))
                if distance < 0.5:
                    flag = 1
                    return flag
        return flag

    def find_only_one(self, child_node):
        for i in range(len(self.node_list)):
            if self.node_list[i].row == child_node.row and self.node_list[i].col == child_node.col:
                return False
        return True

    def find_path_opt(self):
        path = [[self.goal_node.row, self.goal_node.col]]
        last_index = len(self.node_list) - 1
        while self.node_list[last_index].parent is not None:
            node = self.node_list[last_index]
            path.append([node.row, node.col])
            last_index = node.parent
        path.append([self.start_node.row, self.start_node.col])
        return path

    def gen_coord_path(self, path):
        coords = []
        for i in range(len(path)):
            coords.append(grid_to_centre(path[i][::-1], self.params))
        return coords

    def planning(self):
        while True:
            # 随机点
            if random.random() > 0.05:
                sample_point = self.get_sample_point()
            else:
                sample_point = self.goal
            # 距离随机点最近的节点作为父节点
            idx = self.get_near_list_index(sample_point)
            parent_node = self.node_list[idx]
            # 生成子节点
            child_node = self.get_child_node(parent_node,
                                             sample_point)
            # 判断子节点是否越界
            if child_node[0] < 0 or child_node[0] > self.row_num - 1 or child_node[1] < 0 or child_node[1] \
                    > self.col_num - 1:
                continue
            # 避障
            if self.judge_obs(parent_node, child_node):
                continue
            child_node_1 = Node(child_node[0], child_node[1])
            if not self.find_only_one(child_node_1):
                continue
            child_node_1.parent = idx
            self.node_list.append(child_node_1)
            # print(f'new child node: {child_node_1.row}行 {child_node_1.col}列 父节点{child_node_1.parent}')
            # 判断是否接近目标区域
            if abs(child_node_1.row - self.goal_node.row) + abs(child_node_1.col - self.goal_node.col) < 2:
                break
        path = self.find_path_opt()
        print(path)
        coords = self.gen_coord_path(path[::-1])
        logger.info(coords)
        # self.draw_static(path)
        return coords

    def draw_static(self, path):
        plt.figure(figsize=(self.col_num, self.row_num))
        plt.xlim(-1, self.col_num)
        plt.ylim(-1, self.row_num)

        x_tick = np.arange(0, self.col_num, 1)
        y_ticks = np.arange(0, self.row_num, 1)
        plt.xticks(x_tick)
        plt.yticks(y_ticks)
        plt.grid(color='k', linestyle='-', linewidth=0.5)

        ax = plt.gca()  # 获取到当前坐标轴信息
        # ax.xaxis.set_ticks_position('top')  # 将X坐标轴移到上面
        # ax.invert_yaxis()  # 反转Y坐标轴
        for x in range(self.col_num)[::-1]:
            for y in range(self.row_num)[::-1]:
                if self.grid_array[y][x] == 1:
                    plt.scatter(x, y, s=2000, c='k', marker='s')
                else:
                    plt.scatter(x, y, s=2000, c='b', marker='s')

        # plt.scatter([x for x in range(self.row_num - 1)], [y for y in range(self.col_num - 1)], s=2000, c='b', marker='s')
        plt.scatter([xy[1] for xy in path], [xy[0] for xy in path], s=2000, c='y', marker='s')
        plt.scatter(self.start_node.col, self.start_node.row, s=2000, c='r', marker='s')
        plt.scatter(self.goal_node.col, self.goal_node.row, s=2000, c='r', marker='s')
        plt.show()


if __name__ == "__main__":
    obstacle_list = [(119.373225, 32.120244, 20), (119.372865, 32.118738, 10)]
    bounds = [119.37098775602607, 32.11655934651841, 119.37609501851392, 32.12293903313633]
    rrt = RRT(start=[119.372874, 32.118417], goal=[119.373705, 32.12008], bounds=bounds, obstacle_coords=obstacle_list)
    rrt.planning()
    # rrt.draw_static([])
