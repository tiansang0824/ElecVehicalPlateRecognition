"""
用于模板匹配
"""

import numpy as np
import cv2
import os


def read_dir(dir_path):
    """
    返回结构：file_list[ file_set[], file_set[], file_set[], file_set[] ]
    :param templates:
    :param dir_path:
    :return:
    """
    file_list = []
    for file_name in os.listdir(dir_path):
        file_list.append(os.path.join(dir_path + '/' + file_name))
    return file_list


class Matcher:
    templ_img_path = './refer'  # 保存模板图片路径
    templates = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
                 'W',
                 'X', 'Y', 'Z']  # 模板图片索引
    templ_img_list = list()  # 模板图片路径列表
    char_img_path = ''  # 保存字符图片路径
    char_img_path_list = []  # 保存每个单字符图片路径
    char_list = list()  # 保存识别后的字符

    def __init__(self, char_img_path):
        """
        构造函数，获取字符图片总路径以及获取每个单字符的路径
        :param char_img_path:
        """
        self.char_img_path = char_img_path  # 获取字符图片总路径
        """获取单字符路径"""
        # self.char_img_path_list = read_dir(self.char_img_path)

    def load_templ_img_list(self):
        """用于加载模板图片路径列表"""
        self.templ_img_list = []
        for i in range(len(self.templates)):
            templ_img_set = read_dir(self.templ_img_path + '/' + self.templates[i])  # 合成单字符路径
            self.templ_img_list.append(templ_img_set)  # 添加到templ_img_list中。
        print(f'self.templ_img_list: {self.templ_img_list}')

    def single2batch(self, img_path):
        """
        单个字符匹配所有模板
        :param img_path: 单字符路径
        :return: 返回匹配结果（字符）
        """
        """处理待匹配字符"""
        char_img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), 1)  # 获取图片
        char_img = cv2.GaussianBlur(char_img, (3, 3), 0)  # 高斯去噪
        char_img = cv2.cvtColor(char_img, cv2.COLOR_BGR2GRAY)  # 灰度化
        char_img = cv2.threshold(char_img, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]  # 二值化
        """获取模板图片路径列表（已经移动到self.load_templ_img_list）"""
        """ 遍历模板图片，与字符图片进行对比 """
        best_score = []
        for templ_img_set in self.templ_img_list:
            score = list()
            for templ_img_path in templ_img_set:
                templ_img = cv2.imdecode(np.fromfile(templ_img_path, dtype=np.uint8), 1)
                # templ_img = cv2.GaussianBlur(templ_img, (3, 3), 0)
                templ_img = cv2.cvtColor(templ_img, cv2.COLOR_BGR2GRAY)
                templ_img = cv2.threshold(templ_img, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
                result = cv2.matchTemplate(char_img, templ_img, cv2.TM_CCOEFF)
                score.append(result[0][0])
            best_score.append(max(score))
        print(f'best_score: {best_score}')
        matched_char = self.templates[best_score.index((max(best_score)))]
        return matched_char


if __name__ == '__main__':
    m = Matcher('./divide/test12')
    print(m.char_img_path_list)
    m.load_templ_img_list()
    c = m.single2batch('./divide/test12/test12-0.jpg')
    print(f'c: {c}')
