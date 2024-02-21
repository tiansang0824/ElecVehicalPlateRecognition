"""
该文件代码主要用于模板匹配实现字符识别

"""
# 导入所需模块
import cv2
from matplotlib import pyplot as plt
import os
import numpy as np
from PIL import Image


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
    # print(f'指定文件夹下的文件有：{refer_img_list}')  # 测试代码，输出指定文件夹下检查到的所有文件
    return refer_img_list


def reverse_img_color(img):
    """
    该函数用于反转图片的黑白像素。

    该函数通过将图片转换成数组，然后通过取反运算符，将黑白像素反转，
    最后利用PIL.Image的函数将数组还原为图片，并且通过return返回。

    :return:  返回反转后的图片。
    """
    # 使用 bitwise_not 函数反转图像像素
    inverted_image = cv2.bitwise_not(img)  # 调用cv2的函数进行反转
    return inverted_image  # 返回反转后的图片


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
        char_img = cv2.imdecode(np.fromfile(self.imgName, dtype=np.uint8), 1)  # 以合适的方式从文件读取图片
        best_score = []  # 匹配度列表
        words = []  # 模板图片列表
        # 读取所有模板
        for i in range(len(self.template)):
            # print(self.template[i])  # 测试代码，该代码可以输出全部template的内容
            word = read_dir('./refer/' + self.template[i])  # 读取这一轮循环下的全部文件的文件路径
            words.append(word)  # 将读取到的模板图片路径添加到words中。
        # print(f'words: {words[11]}')  # 测试代码，这里会返回第11个字符的所有模板图片的相对路径
        """
        注意：
        现在的words 保存的是所有数字和字母的模板图片路径，
        其中，words的每一个元素都是一个列表，该列表包含了某一个字符的所有模板图片路径。
        """
        # 进行模板匹配
        for word in words:
            score = []
            for w in word:
                # fromfile() 函数读回数据时需要用户指定元素类型，并对数组的形状进行适当修改
                template_img = cv2.imdecode(np.fromfile(w, dtype=np.uint8), 1)  # 读取图片
                template_img = cv2.cvtColor(template_img, cv2.COLOR_BGR2GRAY)
                ret, template_img = cv2.threshold(template_img, 0, 255, cv2.THRESH_OTSU)
                cv2.imshow('template_img', template_img)  # 测试代码
                cv2.waitKey(0)
                height, width = template_img.shape
                tmp_char_img = char_img.copy()  # 避免改变原图片
                tmp_char_img = (tmp_char_img * 255).astype(np.uint8)  # 将原图副本修改为符合模板匹配的8位无符号整型数
                tmp_char_img = cv2.resize(tmp_char_img, (width, height))  # 重置图片宽度高度
                cv2.imshow('img', char_img)
                cv2.waitKey(0)
                result = cv2.matchTemplate(tmp_char_img, template_img, cv2.TM_CCOEFF)  # 返回值越大，相似度越高
                score.append(result[0][0])  # 追加匹配结果
            best_score.append(max(score))  # 将最高匹配结果作为该字符的匹配结果，追加到best_score中
        print(f'best_score: {best_score}')

    def match_multiple_chars(self):
        """
        该函数用于匹配车牌分割后的字符。
        :return:
        """
        pass


if __name__ == '__main__':
    # read_dir('./divide/test12')  # 测试代码：读取指定目录下所有文件的文件路径
    """ 测试代码：反转二值图的黑白像素点
    test_img = cv2.imread('./divide/test12/test12-1.jpg')  # 读取测试图片
    test_img = reverse_img_color(test_img)  # 测试反转像素的函数
    cv2.imshow('test12', test_img)
    cv2.waitKey(0)
    """
    """ 测试代码：读取所有模板图片
    test_img = cv2.imread('./divide/test12/test12-1.jpg')
    m = Mather('test12')
    m.match_single_char(test_img)
    """
    test_img = cv2.imread('D:\project\田桑的车牌识别项目\src\divide\test12\test12-1.jpg')
    m = Mather('test12')
    m.match_single_char()
