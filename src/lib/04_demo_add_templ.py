import numpy as np
import cv2
import os

char_img_path = 'D:/cache/divide/img05/img05-4.jpg'  # 图片路径
templ = '1'  # 目标字符
templ = templ.upper()
order = '1003'  # 文件后缀

char_img = cv2.imdecode(np.fromfile(char_img_path, dtype=np.uint8), 1)
char_img = cv2.GaussianBlur(char_img, (3, 3), 0)
char_img = cv2.cvtColor(char_img, cv2.COLOR_BGR2GRAY)
char_img = cv2.threshold(char_img, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

img_height, img_width = char_img.shape[:2]

char_img = cv2.resize(char_img, (int(img_width/4), int(img_height/4)))

cv2.imshow('char_img', char_img)
cv2.waitKey(0)

cv2.imwrite('../refer/' + templ + '/demo' + order + '.jpg', char_img)
