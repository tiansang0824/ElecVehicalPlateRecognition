import os
import cv2
import numpy as np
import matplotlib.pyplot as plt


def plt_show(img):
    b, g, r = cv2.split(img)
    img = cv2.merge([r, g, b])
    plt.imshow(img)
    plt.show()


def plt_show_gray(img):
    plt.imshow(img, cmap='gray')
    plt.show()


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


def process_and_save(img_path, save_path):
    templ_img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), 1)  # 读取模板图片
    templ_img = cv2.cvtColor(templ_img, cv2.COLOR_BGR2GRAY)  # 转换为灰度图
    ret, templ_img = cv2.threshold(templ_img, 255, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)  # 二值化和阈值处理
    templ_img = cv2.resize(templ_img, (20, 20))
    img_name = img_path.split('/')[-1]
    cv2.imwrite(save_path + img_name, templ_img)


if __name__ == '__main__':
    process_and_save('../divide/test12/test12-3.jpg', '../refer/1/')
