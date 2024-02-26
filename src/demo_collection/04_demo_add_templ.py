import numpy as np
import cv2
import os

char_img_path = '../divide/test12/test12-5.jpg'

img_width = 20
img_height = 20

char_img = cv2.imdecode(np.fromfile(char_img_path, dtype=np.uint8), 1)
char_img = cv2.GaussianBlur(char_img, (3, 3), 0)
char_img = cv2.cvtColor(char_img, cv2.COLOR_BGR2GRAY)
char_img = cv2.threshold(char_img, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

char_img = cv2.resize(char_img, (img_width, img_height))

cv2.imshow('char_img', char_img)
cv2.waitKey(0)

cv2.imwrite('../refer/9/demo1001.jpg', char_img)
