# 导入所需模块
import cv2
import numpy as np
from matplotlib import pyplot as plt
import scipy


class MyDivide(object):
    imgName = ''  # 保存图片名
    imgPath = './position/'  # 图片路径
    dividePath = ('./divide/')  # 分割图片的保存位置

    img = []
    gray = []  # 用于保存灰度图
    binary = []  # 用于保存二值图
    data = []  # 用于以数组的形式保存图片
    len_x = []  # x方向长度
    len_y = []  # y方向长度
    rowPairs = []

    rows = []  # 行数
    cols = []  # 列数

    # 下面的几个属性主要用于竖直方向切割的时候用。
    min_val = 15  # 最小密度，用于筛除较大的噪点

    def __init__(self, name):
        self.imgName = name  # 读取图片名
        self.dividePath = self.dividePath + name.split('-', 1)[0] + '/'  # 设置保存路径（和文件名）
        self.img = cv2.imread(self.imgPath + self.imgName + '-pos.png')  # 到指定文件夹读取文件（定位后的车牌区域图片）

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

        # 测试代码，输出读取到的原始图片
        cv2.imshow('original image', self.img)
        cv2.waitKey(0)

    def bgr2gray(self):
        """
        原始图片转换成灰度图
        :return:
        """
        self.gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)

        cv2.imshow('gray image', self.gray)  # 测试代码，输出灰度图
        cv2.waitKey(0)  # waitKey

        return self.gray

    def gray2binary(self):
        """
        灰度图转换成二值图
        :return:
        """
        ret, self.binary = cv2.threshold(self.gray, 127, 255, cv2.THRESH_BINARY_INV)

        cv2.imshow('binary image', self.binary)  # 测试代码：输出二值图
        cv2.waitKey(0)  # waitKey

        return self.binary

    """
    当前思路：
    进行车牌分割，需要进行水平和竖直方向的分割，
    竖直方向分割的目的是要找到车牌号所在的那几行，水平分割的目的是将字符区域分别划分开来。
    应该使用什么样的方法实现两个方向的分割？
    暂定：竖直方向切分的时候采用密度判断的方法；水平方向切分的时候采用直方图的方式分割。
    """

    def binary2array(self):
        """ 二值图转换成二维数组 """
        self.data = np.array(self.binary)  # 这行代码转换了对象的binary属性，构建了一个NumPy数组并将其存储在self.data中。这里的self.binary应该是二进制数据。
        # 原来的x和y是读取的原图片的尺寸，如果self.img经过修改，则x、y两个数据将不再正确。
        self.len_x = self.data.shape[0]  # 这行代码获取到了data数组的第一维的长度，并将其存储在self.len_x中。
        self.len_y = self.data.shape[1]  # 这行代码获取到了data数组的第二维的长度，并将其存储在self.len_y中。

        print(f'data: {self.data}')  # 测试代码，输出转化后的数组
        print(f'len_x: {self.len_x}, len_y: {self.len_y}')  # 测试代码，输出数组的长宽

        return self.data

    def line_seg(self):
        """
        函数lineSeg, 从二维数组中检测线段的起始和结束位置，并将这些位置存储在rowPairs列表中。
        :return:
        """
        # 初始化变量start_i和end_i，它们用于存储线段的起始和结束位置的行索引。
        start_i = -1
        end_i = -1
        # 初始化空列表rowPairs，用于存储检测到的线段的起始和结束位置的行索引对。
        self.rowPairs = []

        def judge(line_data, length):
            """
            定义局部函数Judge，用来判断线段的像素密度是否满足条件。具体方法为：线段中的白色像素（255）的比例占整个线段的长度的比例是否介于0.2和0.8之间。

            :param line_data: 某行的数据，建议摘自self.data
            :param length: 某行的线段长度，可以直接调用self.len_y。
            :return: 函数返回一个布尔值，表示线段中的白色像素（255）的比例占整个线段的长度的比例是否介于0.2和0.8之间。
            """
            x = (line_data.sum() / 255) / length  # 白色像素点的数量除以总长度
            return 0.8 > x > 0.2  # 按照是否符合规定范围决定返回的bool值为真还是假

        for i in range(self.len_x):  # 逐一判断原图片的每一行
            if judge(self.data[i], self.len_y) and start_i < 0:
                # 如果当前行的线段像素密度满足条件，并且之前没有开始记录线段的起始位置，则将当前行的索引存储在start_i中。
                start_i = i
            elif judge(self.data[i], self.len_y):
                # 如果当前行的线段像素密度满足条件，并且之前已经开始记录线段的起始位置，则将当前行的索引存储在end_i中。
                end_i = i
            elif not judge(self.data[i], self.len_y) and start_i >= 0:
                # 如果当前行的线段像素密度不满足条件，说明，该行有可能是不满足条件的行、或者是需要截取的片段的末尾行。
                # 如果之前已经记录过起始行，说明该行是结束行，
                # 则进行进一步判断该片段宽度是否大于规定的最小宽度（self.min_val）
                if end_i - start_i >= self.min_val:
                    # 判断是否大于最小的字符高度
                    # self.min_val是实例内的常数（min_val = 10）用于避免切分噪音
                    self.rowPairs.append((start_i, end_i))  # 如果大于最小高度，则视作是字符段，追加到self.rowPairs中。
                start_i = -1  # 重置起始位置（行号）
                end_i = -1  # 重置结束位置（行号）

        print(f'self.rowPairs: {self.rowPairs}')  # 测试代码，输出截取到的字符区域（竖直方向）

    def show_details(self):
        cv2.imshow("img", self.img)  # 展示图片
        cv2.imshow('gray', self.gray)  # 展示图片
        cv2.imshow('binary', self.binary)  # 展示图片
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def show_vertical_segment(self):
        """
        输出数值方向的切片结果
        :return:
        """
        for pair in self.rowPairs:
            # pair表示每一个配对
            start_row = pair[0]
            end_row = pair[1]
            tmp_image = self.binary[start_row:end_row, :]
            cv2.imshow('tmp img', tmp_image)
            cv2.waitKey(0)


if __name__ == '__main__':
    md = MyDivide('test12-1')  # 通过图片名读取图片
    md.bgr2gray()  # 转换成灰度图
    md.gray2binary()  # 转换成二值图
    md.binary2array()  # 转换成数组
    md.line_seg()  # 切分字符位置
    md.show_vertical_segment()  # 测试代码：输出竖直切分后的图片部分
