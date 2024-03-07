"""
单字符模板匹配测试
"""
import cv2
import numpy as np
import matplotlib.pyplot as plt
from tool_kit_show_img import *

char_img_path = '../divide/test12/test12-0.jpg'  # 字符图片路径
# templ_img_path = '../refer/M/m_02.jpg'  # 模板图片路径 3572736
templ_img_path = '../refer/M/demo1001.jpg'  # 模板图片路径
char_img = cv2.imdecode(np.fromfile(char_img_path, dtype=np.uint8), 1)  # 读取字符图片
templ_img = cv2.imdecode(np.fromfile(templ_img_path, dtype=np.uint8), 1)  # 读取模板图片

"""测试代码"""
plt_show(char_img)  # 展示字符图片
plt_show(templ_img)  # 展示模板图片

"""处理字符图片"""
char_img = cv2.GaussianBlur(char_img, (3, 3), 0)  # 高斯去噪
char_img = cv2.cvtColor(char_img, cv2.COLOR_BGR2GRAY)  # 转换成灰度图
ret, char_img = cv2.threshold(char_img, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)  # 二值化并且转为黑底白字
# ret2, char_img = cv2.threshold(char_img, 0, 255, cv2.THRESH_OTSU)  # 自适应阈值处理

"""处理模板图片"""
templ_img = cv2.cvtColor(templ_img, cv2.COLOR_BGR2GRAY)
ret3, templ_img = cv2.threshold(templ_img, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)  # 二值化并且转为黑底白字
# ret4, templ_img = cv2.threshold(templ_img, 0, 255, cv2.THRESH_OTSU)

"""测试代码"""
plt_show_gray(char_img)
plt_show_gray(templ_img)

"""调整字符图片大小"""
height, width = templ_img.shape[:2]
char_img = cv2.resize(char_img, (width, height))

"""测试代码：输出字符图片和模板图片的尺寸"""
c_height, c_width = char_img.shape
print(f'模板图片的尺寸为：{height}x{width}')
print(f'字符图片尺寸为：{c_height}x{c_width}')
plt_show_gray(char_img)
plt_show_gray(templ_img)

"""进行模板匹配"""
result = cv2.matchTemplate(char_img, templ_img, cv2.TM_CCOEFF)
print(f'result: {result}')
