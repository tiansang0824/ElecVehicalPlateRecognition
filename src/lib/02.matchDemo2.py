"""
OpenCV模板匹配测试代码2.0
与1.0版本不同的是，2.0版本会使用多张模板图片与单个字符图片做对比

"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import tool_kit_show_img as my_tools

"""读取和处理字符图片"""
char_img_path = '../divide/test12/test12-3.jpg'  # 字符图片路径
char_img = cv2.imdecode(np.fromfile(char_img_path, dtype=np.uint8), 1)  # 从路径中读取图片
char_img = cv2.GaussianBlur(char_img, (3, 3), 0)  # 高斯去噪
char_img = cv2.cvtColor(char_img, cv2.COLOR_BGR2GRAY)  # 转换为灰度图
ret, char_img = cv2.threshold(char_img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)  # 二值化

"""测试代码：检查处理完的字符图片"""
my_tools.plt_show_gray(cv2.resize(char_img, (20, 20)))

"""
获取模板图片（路径）列表
获取到的模板列表结构是：
templ_img_list[ templ_img_set[templ_img_path, templ_img_path, ...], templ_img_set[templ_img_path, templ_img_path, ...], ...  ]
"""
templ_img_path = '../refer'  # 模板图片总路径
templates = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
             'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W',
             'X', 'Y', 'Z']
templ_img_list = []  # 模板图片（路径）列表
for i in range(len(templates)):
    templ_img_set = my_tools.read_dir(templ_img_path + '/' + templates[i])
    templ_img_list.append(templ_img_set)

"""测试代码：输出模板图片列表"""
test_count = 0
for templ_img_set in templ_img_list:
    for templ_img_path in templ_img_set:
        test_count += 1
        if test_count % 10 == 0:
            print(templ_img_path)


"""遍历所有模板图片，与字符图片进行模板匹配"""
best_score = list()
for templ_img_set in templ_img_list:
    score = list()
    for templ_img_path in templ_img_set:  # 现在templ_img就是每一个模板图片的路径
        templ_img = cv2.imdecode(np.fromfile(templ_img_path, dtype=np.uint8), 1)  # 读取模板图片
        # templ_img = cv2.GaussianBlur(templ_img, (3, 3), 0)  # 高斯去噪
        templ_img = cv2.cvtColor(templ_img, cv2.COLOR_BGR2GRAY)  # 转换为灰度图
        ret, templ_img = cv2.threshold(templ_img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)  # 二值化和阈值处理
        result = cv2.matchTemplate(char_img, templ_img, cv2.TM_CCOEFF)
        score.append([result[0][0], templ_img_path])
    """测试代码：输出每组模板中匹配度最高的图片路径"""
    best_score.append(max(score, key=lambda x: x[0]))

"""检查输出结果"""
print(f'best_score：{best_score}')
best_index = best_score.index(max(best_score, key=lambda x: x[0]))
print(f'index of best score：{best_index}')
print(f'templ of best score: {best_score[best_index]}')
print(f'best matched char: {templates[best_index]}')
