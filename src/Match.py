"""
该文件代码主要用于模板匹配实现字符识别

"""
# 导入所需模块
import cv2
from matplotlib import pyplot as plt
import os
import numpy as np


def read_dir(dir_name):
    """
    读取一个文件夹下的所有文件
    :param dir_name: 文件夹名称、路径
    :return: 返回一个集合，包含指定文件夹下所有文件的路径（字符串）
    """
    refer_img_list = []  # 图片列表
    for filename in os.listdir(dir_name):
        # print(f'file name: {filename}')  # 测试代码
        # img = cv2.imread(dir_name + '/' + filename)  # 测试代码：图片路径
        refer_img_list.append(dir_name + '/' + filename)
    print(f'指定文件夹下的文件有：{refer_img_list}')  # 测试代码，输出指定文件夹下检查到的所有文件
    return refer_img_list


class Mather(object):
    imgName = ''  # 图片读取位置

    # 注意：下面的模板中，删掉了中文字符（因为在电动车车牌识别中不需要中文字符）
    template = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W',
                'X', 'Y', 'Z']

    def __init__(self, name):
        self.imgName = name  # 读取图片位置（文件夹）

    def match_single_char(self):
        """
        该函数用于模板匹配单个字符，并且返回匹配结果（仅含有一个字符的字符串变量）
        :return:
        """
        """
        单字符匹配流程：
        - 创建变量best_score用于保存匹配度，这个变量用来保存目标字符和每一个模板字符的匹配度（不是模板字符下的每一个模板图片）
        - 通过两层循环读取所有模板
        - 对比每一个模板和目标字符的匹配程度
        """
        best_score = []  # 匹配度列表

    def match_multiple_chars(self):
        """
        该函数用于匹配车牌分割后的字符。
        :return:
        """
        pass


if __name__ == '__main__':
    read_dir('./divide/test12')
