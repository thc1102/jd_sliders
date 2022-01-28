import random
import numpy as np


class Track:
    """
    轨迹生成算法类
    """

    def __init__(self, ease_code=None):
        """
        初始化滑块轨迹算法
        :param ease_code: 方法get_tracks1的数据生成函数,可选择1,2,3,如果不传入则随机使用
        """
        if ease_code is None:
            ease_code = random.randint(1, 3)
        if ease_code == 1:
            self.ease_func = self.__ease_out_quad
        elif ease_code == 2:
            self.ease_func = self.__ease_out_quart
        elif ease_code == 3:
            self.ease_func = self.__ease_out_expo
        else:
            self.ease_func = self.__ease_out_quad

    @staticmethod
    def __ease_out_quad(x):
        return 1 - (1 - x) * (1 - x)

    @staticmethod
    def __ease_out_quart(x):
        return 1 - pow(1 - x, 4)

    @staticmethod
    def __ease_out_expo(x):
        if x == 1:
            return 1
        else:
            return 1 - pow(2, -10 * x)

    def get_tracks1(self, distance, seconds):
        """
        根据轨迹离散分布生成的数学 生成
        参考文档  https://www.jianshu.com/p/3f968958af5a
        :param distance: 缺口位置
        :param seconds:  时间
        :return: 轨迹数组
        """
        tracks = [0]
        offsets = [0]
        for t in np.arange(0.0, seconds, 0.1):
            offset = round(self.ease_func(t / seconds) * distance)
            tracks.append(offset - offsets[-1])
            offsets.append(offset)
        return tracks

    @staticmethod
    def get_tracks2(distance):
        """
        根据加减速为主的物理学生成 方式
        匀变速运动基本公式：
        ①：v=v0+at
        ②：s=v0t+½at²
        ③：v²-v0²=2as
        :param distance: 偏移量
        :return: 移动轨迹
        """
        # 移动轨迹
        tracks = []
        # 当前位移
        current = 0
        # 减速阈值
        mid = distance * 4 / 5
        # 计算间隔
        t = 0.3
        # 初速度
        v = 0

        while current < distance:
            if current < mid:
                # 加速度为正
                a = random.uniform(5, 8)
            else:
                # 加速度为负
                a = random.uniform(8, 10) * -1
            # 初速度v0
            v0 = v
            # 当前速度v = v0 + at
            v = v0 + a * t
            # 移动距离x = v0t + 1/2 * a * t^2
            move = v0 * t + 1 / 2 * a * t * t
            # 当前位移
            current += move
            # 加入轨迹
            tracks.append(round(move, 2))
        # 计算位置的差值
        offset_move = round(distance - current, 2)
        # 获取列表后3/5的长度
        offset_len = round(len(tracks) * 3 / 5)
        # 计算每段分散差值
        disperse_move = round(offset_move / offset_len, 2)
        # 把差值写入列表
        for i in range(offset_len):
            list_index = (i + 1) * -1
            list_value = tracks[list_index] + disperse_move
            tracks[list_index] = round(list_value, 2)
        return tracks
