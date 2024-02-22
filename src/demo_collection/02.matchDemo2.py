"""
本段demo测试的内容是，遍历多张模板图片，与字符图片依次进行模板匹配，并且返回匹配结果

"""
import cv2
import numpy as np
import os


def read_dir(dir_path):
    """
    该函数用于批量读取某个字符的所有模板。
    :param dir_path:
    :return:
    """
    img_list = []
    for filename in os.listdir(dir_path):
        img_list.append(dir_path + '/' + filename)
    return img_list


char_img_path = '../divide/test12/test12-2.jpg'
char_img = cv2.imdecode(np.fromfile(char_img_path), 1)  # 读取字符图片
char_img = cv2.cvtColor(char_img, cv2.COLOR_BGR2GRAY)
ret, char_img = cv2.threshold(char_img, 0, 255, cv2.THRESH_OTSU)

templates = [
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
    'Z'
]  # 用于存放模板的列表

words = []  # 用于存放模板图片路径的列表
for i in range(len(templates)):
    word = read_dir('../refer/' + templates[i])  # word用于存放某个字符的全部模板图片的路径
    words.append(word)  # 执行完for循环后，words应该是一个列表的列表

# 测试代码：输出读取到的所有的模板图片的路径
for word in words:
    for w in word:
        print(w)

best_score = []
# 循环所有图片，和字符图片进行模板吧匹配
for word in words:
    score = []
    for w in word:
        # 针对每一个字符，首先读取图片
        templ_img = cv2.imdecode(np.fromfile(w, np.uint8), 1)  # 读取模板图片
        templ_img = cv2.cvtColor(templ_img, cv2.COLOR_BGR2GRAY)
        ret, templ_img = cv2.threshold(templ_img, 0, 255, cv2.THRESH_OTSU)
        # 重置字符图片的尺寸
        height, width = templ_img.shape[:2]
        char_img_copy = char_img.copy()
        char_img_copy = cv2.resize(char_img_copy, (width, height))
        # 测试输出
        # cv2.imshow('char_img', char_img_copy)
        # cv2.imshow('template', templ_img)
        # cv2.waitKey(0)
        # print(f'size of char_img: {char_img_copy.shape}')
        # print(f'size of templ_img: {templ_img.shape}')
        # 进行模板匹配
        result = cv2.matchTemplate(char_img_copy, templ_img, cv2.TM_CCOEFF)
        # 测试代码：
        # print(f'单次测试结果为：{result}')
        # 加入到score
        score.append(result[0][0])
    # 将最高匹配项加入到best_score中
    best_score.append(max(score))

print(f'best_score：{best_score}')
print(f'max of best_score[]：{max(best_score)}')
i = best_score.index(max(best_score))
print(f'index of max：{best_score.index(max(best_score))}')
print(f'in templates: {templates[i]}')
