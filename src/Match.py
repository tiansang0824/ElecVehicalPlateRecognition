import os
import numpy as np
import cv2
import matplotlib.pyplot as plt


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
    templates = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
                 'W', 'X', 'Y', 'Z']
    templ_path = './refer/'  # 模板图片路径
    char_img_path_list = ''  # 字符图片路径
    answer = ''

    def __init__(self, path):
        """
        构造函数
        :param path: 字符图片路径
        """
        self.char_img_path_list = read_dir(path)

    def single2all(self, char_image_path, template_path):
        """
        一个字符图片匹配全部模板。
        :param char_image_path:
        :param template_path:
        :return:
        """
        """ 读取和处理字符图片 """
        img = cv2.imdecode(np.fromfile(char_image_path, dtype=np.uint8), 1)  # 读取图片
        img = cv2.GaussianBlur(img, (3, 3), 0)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        char_img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        """ 读取全部模板图片路径 """
        templ_list = list()
        for i in range(len(self.templates)):
            templ_set = read_dir(template_path + self.templates[i])
            templ_list.append(templ_set)
        # print(templ_list)
        """ 遍历模板，进行模板匹配 """
        best_scores = list()
        for templ_set in templ_list:
            scores = list()
            for single_templ_img_path in templ_set:
                """ 读取和处理模板图片 """
                templ = cv2.imdecode(np.fromfile(single_templ_img_path, dtype=np.uint8), 1)
                templ = cv2.GaussianBlur(templ, (3, 3), 0)
                templ = cv2.cvtColor(templ, cv2.COLOR_BGR2GRAY)
                templ = cv2.threshold(templ, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
                """ 修改字符图片的尺寸 """
                height, width = templ.shape
                char_img = cv2.resize(char_img, (width, height))
                """ 模板匹配 """
                result = cv2.matchTemplate(char_img, templ, cv2.TM_CCOEFF)[0][0]
                scores.append(result)
            print(f'max score: {max(scores): 13.2f} in {scores}')
            best_scores.append(max(scores))
        print(f'>> best_score的内容为: {best_scores}')
        print(f'>> best_scores的最大值为: {max(best_scores)}, 对应的下标是：{best_scores.index(max(best_scores))}')
        print(f'>> 待确认字符为: {self.templates[best_scores.index(max(best_scores))]}')
        return self.templates[best_scores.index(max(best_scores))]

    def match_all(self):
        """
        该函数用于一次性匹配所有字符。

        有了single2all以后，这个函数的实现就简单很多了
        1. 找到所有字符图片的路径
        2. 遍历每个路径，对每个路径对应的字符图片应用single2all()函数。
        3. 收集每次遍历的识别结果。

        :return: 返回一个列表，该列表中的每一个元素对应一个识别出来的字符。
        """
        self.answer = list()
        char_img_set = self.char_img_path_list[0:len(self.char_img_path_list) - 1]  # char_img_set 用于保存单字符字符图片
        # print(f'char_img_set: {char_img_set}')
        for char_img_path in char_img_set:
            character = self.single2all(char_img_path, self.templ_path)  # 对单个字符进行比较
            self.answer.append(character)
        print(f'>> answer is : {self.answer}')

    def get_final_answer(self):
        return ''.join(self.answer)


if __name__ == '__main__':
    m = Matcher('./divide/test12')
    print(m.char_img_path_list)
    # m.single2all('./divide/test12/test12-4.jpg', './refer/')
    m.match_all()
    final_answer = m.get_final_answer()
    print(f'final answer is : {final_answer}')
