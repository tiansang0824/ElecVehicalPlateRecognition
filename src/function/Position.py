# -*- coding: utf-8 -*-

import cv2
import math
import numpy as np
from scipy import misc, ndimage
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = ['Simsun']


class MyPosition:
    # 图片路径
    imgName = ''
    # 保存图片路径
    positionPath = 'D:/cache/position/'
    # 根据原图片名确定,该变量出现在构造函数中.
    positionName = ''

    img = []  #
    gray = []  #
    gaussian = []
    median = []
    sobel = []
    binary = []
    dilation = []
    dilation2 = []
    erosion = []
    closed = []
    result = []

    len_x = 0  #
    len_y = 0  #

    def __init__(self, name):
        """
        构造函数,需要传入原始图片路径
        :param name: 原始图片路径
        """
        plt.rcParams['font.family'] = ['Simsun']
        # 读取原始图片
        self.img = cv2.imread(name)
        # 重置图片尺寸
        # [rows, cols] = self.img.shape[:2]
        # self.img = cv2.resize(self.img, (int(cols / 5), int(rows / 5)))
        # 设置图片保存位置
        # name.split('.')[-2] 表示的是"文件路径+文件名"(文件扩展名前面的一部分)的组合
        # 在此基础上,通过 '/' 分割字符串,并且取最后一个元素,得到的是文件名,
        # 在通过手动添加文件名后缀和文件名扩展名,创建出保存位置
        self.positionName = (name.split('.')[-2]).split('/')[-1] + '-pos.png'
        # 获取原图的宽高比例
        self.len_x = self.img.shape[0]
        self.len_y = self.img.shape[1]

    def remove_noise(self, img):
        """
        旧的名字是`RemoveNoise`,以防万一,在这里记录一下.

        :param img: 去噪图片,建议直接采用self.img
        :return:
        """
        plt.rcParams['font.family'] = ['Simsun']
        # 加入图片
        self.img = img

        # 灰度化处理
        self.gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 高斯平滑 去噪声
        # 去噪图片,卷积核(高斯核)宽高,x/y方向的标准差,边界填充方法(默认:使用图像边界像素填充)
        self.gaussian = cv2.GaussianBlur(self.gray, (3, 3), 0, 0, cv2.BORDER_DEFAULT)
        # 去除椒盐噪声
        self.gaussian = cv2.medianBlur(self.gaussian, 5)

        # 中值滤波
        self.median = cv2.medianBlur(self.gaussian, 5)

        # Sobel算子 XY方向求梯度
        x = cv2.Sobel(self.median, cv2.CV_32F, 1, 0, ksize=3)  # X方向
        y = cv2.Sobel(self.median, cv2.CV_32F, 0, 1, ksize=3)  # Y方向
        gradient = cv2.subtract(x, y)
        self.sobel = cv2.convertScaleAbs(gradient)  # 得到sobel算子检测结果

        # 二值化
        blurred = cv2.GaussianBlur(self.sobel, (9, 9), 0)  # 再进行一次高斯去噪
        ret, self.binary = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY)

        # 膨胀和腐蚀操作的核函数
        element1 = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 1))
        element2 = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 7))

        # 第一次膨胀
        self.dilation = cv2.dilate(self.binary, element2, iterations=1)
        # 腐蚀
        self.erosion = cv2.erode(self.dilation, element1, iterations=1)

        # 第二次膨胀
        self.dilation2 = cv2.dilate(self.erosion, element2, iterations=3)

        # 闭运算
        # 建立一个椭圆核函数
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25))
        # 执行图像形态学操作
        self.closed = cv2.morphologyEx(self.binary, cv2.MORPH_CLOSE, kernel)
        self.closed = cv2.erode(self.closed, None, iterations=4)
        self.closed = cv2.dilate(self.closed, None, iterations=4)

    def get_profile(self):
        """
        原名字是: `getProfile`, 做一次记录
        :return: 返回车牌所在区域图片
        """
        plt.rcParams['font.family'] = ['Simsun']
        # 寻找边界
        # 依据图片[self.closed:闭操作处理结果图];
        # 轮廓提取模式[RETR_LIST:提取所有轮廓];
        # 轮廓近似方法[CHAIN_APPROX_SIMPLE:简化轮廓只保留端点信息]
        # cnts是轮廓组成的列表,
        # 第二个参数是层次结构参数,由于后续不会使用,所以直接忽略掉
        (cnts, _) = cv2.findContours(self.closed.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        # 根据轮廓围成面积进行排序
        # 第一个参数是轮廓列表
        # 第二个参数是计算轮廓面积
        # 第三个参数表示降序(反转)排列
        # 最后获取面积最大的轮廓
        c = sorted(cnts, key=cv2.contourArea, reverse=True)[0]
        # 计算c的最小外接矩形
        rect = cv2.minAreaRect(c)
        # 将最小外接矩形的四个顶点信息保存到box中
        # cv2.boxPoints() 用于获取顶点坐标
        # np.int0()用于将坐标值转化为整数值
        box = np.int0(cv2.boxPoints(rect))
        # 下面是测试代码,用于绘制图形,
        # 在原图的复制品中绘制矩形,
        # 复制原图,避免损坏原图; 将 box 的信息包装到列表中; -1表示绘制所有轮廓; 设定轮廓颜色; 设定轮廓粗细
        final_img = cv2.drawContours(self.img.copy(), [box], -1, (0, 0, 255), 3)
        # cv2 展示图片
        cv2.imshow('final img with max contour drawn on', final_img)  # 过程测试代码
        # 获取box的四个顶点坐标
        up = max(min(box[i][1] for i in range(4)), 0)
        down = min(max(box[i][1] for i in range(4)), self.len_x)
        left = max(min(box[i][0] for i in range(4)), 0)
        right = min(max(box[i][0] for i in range(4)), self.len_y)
        # my_img 用于存储车牌所在区域的图片
        my_img = self.img[up:down, left:right]
        # 将车牌所在区域图片赋值给slef.result
        self.result = my_img
        # 返回车牌所在区域图片
        return my_img

    def get_details(self):
        """
        原函数名: getDetails, 特此标记
        该函数用于展示处理过程的每一个步骤的处理结果
        :return:
        """
        plt.rcParams['font.family'] = ['Simsun']
        # 如果经过处理之后的图像大小与原始图像大小不一致，则输出提示信息表示处理未完成。
        if self.closed.shape[:2] != self.img.shape[:2]:
            print("没有处理完成", self.closed.shape, self.img.shape)
        # 设置plt的字体参数
        plt.rcParams['font.family'] = ['Simsun']
        # plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        titles = [u"原图(BGR格式)", '灰度图', '高斯降噪',
                  '中值滤波', '边缘检测', '二值化',
                  '第一次膨胀', '腐蚀', '第二次膨胀']
        images = [self.img, self.gray, self.gaussian,
                  self.median, self.sobel, self.binary,
                  self.dilation, self.erosion, self.closed]
        # 封装准备展示的图像
        for i in range(9):
            # 使用 plt.subplot() 函数将每张图像以网格形式显示在 3x3 的子图中。
            plt.subplot(3, 3, i + 1)
            plt.imshow(images[i], 'gray')
            plt.title(titles[i])
            plt.xticks([]), plt.yticks([])
        plt.show()

    def Rotate(self):
        """
        用于旋转的函数
        :return:
        """
        plt.rcParams['font.family'] = ['Simsun']
        # 将车牌区域如片转为灰度图
        gray = cv2.cvtColor(self.result, cv2.COLOR_BGR2GRAY)
        # Canny边缘检测
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        # 霍夫变换
        # 霍夫变换检测直线,于是 lines 就代表了图像中的边缘
        lines = cv2.HoughLines(edges, 1, np.pi / 180, 0)
        # 遍历检测到的直线,计算直线的斜率
        rotate_angle = 0
        for rho, theta in lines[0]:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))
            if x1 == x2 or y1 == y2:
                continue
            t = float(y2 - y1) / (x2 - x1)
            rotate_angle = math.degrees(math.atan(t))
            # 根据斜率的值，函数确定需要旋转的角度。
            # 如果角度大于45度，则将其调整为-90加上原始角度。
            # 如果角度小于-45度，则将其调整为90加上原始角度。
            if rotate_angle > 45:
                rotate_angle = -90 + rotate_angle
            elif rotate_angle < -45:
                rotate_angle = 90 + rotate_angle
        # 函数使用ndimage.rotate函数对图像进行旋转，并返回旋转后的图像。
        # rotate_img = ndimage.rotate(self.result, rotate_angle,mode='constant',cval = 255.0)
        rotate_img = ndimage.rotate(self.result, rotate_angle, mode='nearest')
        self.img = rotate_img
        return rotate_img

    def save(self):
        cv2.imwrite(self.positionPath + self.positionName, self.result)
        # cv2.imwrite(self.positionPath + self.positionName, self.img)


if __name__ == '__main__':
    """
    下面是一个调用demo,用作测试
    
    测试数据记录：
    - test01可用
    - img23可用
    - img05可用
    - img07可用
    - img08可用
    - img10可用
    - img12可用
    - img13 ok
    - img14 ok f83956
    - img16 ok 292256
    - img17 ok 292256
    - img19 ok L58720
    - img20 err
    - img22 err
    - img23 ok L51802
    """
    plt.rcParams['font.family'] = ['Simsun']
    # 创建实例,并且传入图片位置
    # pos是创建出来的实例
    pos = MyPosition('../images/test01.jpg')
    # 去噪处理
    pos.remove_noise(pos.img)
    # 找到车牌位置
    # get profile 得到的是车牌的位置，即现在的img保存的是车牌照片
    img = pos.get_profile()
    # 输出处理过程
    pos.get_details()
    # 展示如片
    cv2.imshow('plate area after process 1', img)
    cv2.waitKey(0)  # 避免cv展示图片闪退
    # 旋转车牌区域图片
    img = pos.Rotate()
    # 车牌图片去噪声
    pos.remove_noise(img)
    # 新图片重新获取车牌区域
    img = pos.get_profile()
    # 输出处理过程
    pos.get_details()
    # 展示图片
    cv2.imshow('plate area after process 2', img)
    # 保存图片
    pos.save()
    # 等待用户处理
    cv2.waitKey(0)
