import numpy as np
import cv2
import os
import tool_kit_show_img as tools

img_path = '../divide/test12/test12-0.jpg'
templ_path = '../refer/M/'


def single2single():
    """

    :return:
    """
    """处理字符图片"""
    char_img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), 1)
    char_img = cv2.GaussianBlur(char_img, (3, 3), 0)
    char_img = cv2.cvtColor(char_img, cv2.COLOR_BGR2GRAY)
    char_img = cv2.threshold(char_img, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    char_img = cv2.resize(char_img, (20, 20))
    tools.plt_show_gray(char_img)
    """获取单字符所有模板图片"""
    templ_list = tools.read_dir(templ_path)
    print(templ_list)
    """遍历所有模板图片进行模板匹配"""
    for templ in templ_list:
        templ_img = cv2.imdecode(np.fromfile(templ_path, dtype=np.uint8), 1)
        templ_img = cv2.GaussianBlur(templ_img, (3,3), 0)
        templ_img = cv2.cvtColor(templ_img, cv2.COLOR_BGR2GRAY)
        templ_img = cv2.threshold(templ_img, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        tools.plt_show_gray(templ_img)
        result = cv2.matchTemplate(char_img, templ_img, cv2.TM_CCOEFF)
        print(result)

single2single()
