"""
这个demo用来将字符图片和指定文件夹内的模板（某个单一字符的所有模板）进行匹配
"""
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import tool_kit_show_img as my_tools

"""读取和处理字符图片"""
char_img_path = '../divide/test12/test12-1.jpg'  # 字符图片路径
char_img = cv2.imdecode(np.fromfile(char_img_path, dtype=np.uint8), 1)  # 从路径中读取图片
char_img = cv2.GaussianBlur(char_img, (3, 3), 0)  # 高斯去噪
char_img = cv2.cvtColor(char_img, cv2.COLOR_BGR2GRAY)  # 转换为灰度图
ret, char_img = cv2.threshold(char_img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)  # 二值化

"""测试代码：检查处理完的字符图片"""
my_tools.plt_show_gray(cv2.resize(char_img, (20, 20)))

"""获取所有模板路径"""
templ_img_path = '../refer/2'  # 模板图片总路径
templ_img_list = my_tools.read_dir(templ_img_path)  # 创建列表

"""测试输出所有模板路径"""
print(f'templ_img_list: {templ_img_list}')

"""逐个进行模板匹配"""
scores = list()
for templ_img_path in templ_img_list:
    """处理模板图片"""
    templ_img = cv2.imdecode(np.fromfile(templ_img_path, dtype=np.uint8), 1)  # 读取模板图片
    templ_img = cv2.cvtColor(templ_img, cv2.COLOR_BGR2GRAY)  # 转换为灰度图
    ret, templ_img = cv2.threshold(templ_img, 255, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)  # 二值化和阈值处理
    """测试输出模板图片"""
    # my_tools.plt_show_gray(templ_img)
    result = cv2.matchTemplate(char_img, templ_img, cv2.TM_CCOEFF)
    scores.append(result[0][0])

"""测试输出所有模板匹配结果"""
print(f'scores: {scores}')
print(f'best: {max(scores)}')