# 导入所需模块
import cv2
from matplotlib import pyplot as plt


class MyDivide(object):
    imgName = ''  # 保存图片名
    imgPath = './position/'  # 图片路径
    dividePath = ('./divide/')  # 分割图片的保存位置

    img = []
    gray = []
    binary = []
    rows = []
    cols = []
    rowPairs = []

    def __init__(self, name):
        self.imgName = name  # 读取图片名
        self.dividePath = self.dividePath + name.split('-', 1)[0] + '/'  # 设置保存路径（和文件名）
        self.img = cv2.imread(self.imgPath + self.imgName)  # 到指定文件夹读取文件（定位后的车牌区域图片）

        x = self.img.shape[0]  # 获取图片rows
        y = self.img.shape[1]  # 获取图片cols
        self.rowPairs = []  # 原始变量名是 rowPairs

        # 对于太小的图片进行放大
        """
        判断图片尺寸，
        如果宽度小于360，则将宽度放大到360，并且等比例放大高度
        如果高度小于360，则将高度放大到360，并且等比例放大宽度
        并且将修改后的图片覆盖原来的self.img
        """
        if x < 360:
            self.img = cv2.resize(self.img, (360, 360 * x // y))
        elif y < 360:
            self.img = cv2.resize(self.img, (360 * y // x, 360))

    def bgr2gray(self):
        self.gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        return self.gray

    def gray2binary(self):
