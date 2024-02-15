"""
该python文件用于字符分割

"""
import cv2
import numpy as np
import os
import shutil


class MyDivide:
    imgName = ''  # 图片名
    imgPath = './position/'  # 图片位置
    dividePath = './divide/'  # 分割后的位置

    img = []  # 读入的图片
    gray = []  # 灰度图
    binary = []  # 二值图
    data = []  # 图片转换成array
    len_x = 0  # data的高度
    len_y = 0  # data的宽度
    rowPairs = []  # 行分割后的结果

    min_val = 10  # 最小字符高度，防止切分噪音
    dsize_x = 16  # 分割后的图像高度
    dsize_y = 16  # 分割后图像宽度

    def __init__(self, name):
        """
        构造函数
        :param name: 图片名
        """
        self.imgName = name  # 将图片名存入实例
        """
        配置分割图片的保存路径，以及通过图片名读取被定位后的图片
        """
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

    def Bgr2Gray(self):
        """
        封装转换灰度图的函数
        :return:
        """
        self.gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        return self.gray

    def Gray2Binary(self):
        """
        封装转换二值图的函数
        @todo: 二值图转换函数可以优化，这里先放放。
        :return:
        """
        GrayImageF1, self.binary = cv2.threshold(self.gray, 127, 255, cv2.THRESH_BINARY_INV)
        return self.binary

    def Binary2Array(self):
        """

        :return:
        """
        self.data = np.array(self.binary)  # 这行代码转换了对象的binary属性，构建了一个NumPy数组并将其存储在self.data中。这里的self.binary应该是二进制数据。
        # 原来的x和y是读取的原图片的尺寸，如果self.img经过修改，则x、y两个数据将不再正确。
        self.len_x = self.data.shape[0]  # 这行代码获取到了data数组的第一维的长度，并将其存储在self.len_x中。
        self.len_y = self.data.shape[1]  # 这行代码获取到了data数组的第二维的长度，并将其存储在self.len_y中。

    def lineSeg(self):
        """
        函数lineSeg, 从二维数组中检测线段的起始和结束位置，并将这些位置存储在rowPairs列表中。

        :return:
        """
        # 初始化变量start_i和end_i，它们用于存储线段的起始和结束位置的行索引。
        start_i = -1
        end_i = -1
        # 初始化空列表rowPairs，用于存储检测到的线段的起始和结束位置的行索引对。
        self.rowPairs = []

        def Judge(linedata, length):
            """
            该函数用于竖向切分图片，从而将字符行从原图片中提取出来

            定义局部函数Judge，用来判断线段的像素密度是否满足条件。
            具体方法为：线段中的白色像素（255）的比例占整个线段的长度的比例是否介于0.2和0.8之间。
            函数返回一个布尔值。

            :param linedata:
            :param length: 线段长度
            :return: 函数返回一个布尔值，表示线段中的白色像素（255）的比例占整个线段的长度的比例是否介于0.2和0.8之间。
            """
            x = (linedata.sum() / 255) / length  # 白色像素点的数量除以总长度
            return 0.8 > x > 0.2  # 按照是否符合规定范围决定返回的bool值为真还是假

        for i in range(self.len_x):  # 逐一判断原图片的每一行
            if Judge(self.data[i], self.len_y) and start_i < 0:
                # 如果当前行的线段像素密度满足条件，并且之前没有开始记录线段的起始位置，则将当前行的索引存储在start_i中。
                start_i = i
            elif Judge(self.data[i], self.len_y):
                # 如果当前行的线段像素密度满足条件，并且之前已经开始记录线段的起始位置，则将当前行的索引存储在end_i中。
                end_i = i
            elif not Judge(self.data[i], self.len_y) and start_i >= 0:
                # 如果当前行的线段像素密度不满足条件，并且之前已经开始记录线段的起始位置，则进行进一步判断
                if end_i - start_i >= self.min_val:
                    # 判断是否大于最小的字符高度
                    # self.min_val是实例内的常数（min_val = 10）用于避免切分噪音
                    self.rowPairs.append((start_i, end_i))  # 如果大于最小高度，则视作是字符段，追加到self.rowPairs中。
                start_i = -1  # 重置起始位置（行号）
                end_i = -1  # 重置结束位置（行号）

    def columnSeg(self):
        """
        按列进行切分

        从二维数组中检测列的起始和结束位置，并将每个列的图像保存到本地文件中。

        对按行切分后的图片进行该操作，即可实现对字符的横向切割。

        :return:
        """
        # 如果指定路径（self.dividePath）下的文件夹已经存在，那么就删除该文件夹及其内容。这是为了确保每次运行程序时，都能从头开始保存图像。
        if os.path.exists(self.dividePath):
            shutil.rmtree(self.dividePath)
        os.mkdir(self.dividePath)  # 创建一个新的文件夹，用于保存划分后的图像。
        # 初始化变量start_j和end_j为-1，它们用于存储列的起始和结束位置的列索引。
        start_j = -1  # 列起始索引
        end_j = -1  # 列结束索引
        min_val = 5  # 最小列长的阈值
        num = 0  # 初始化计数器num，用于生成图像的文件名。
        for start, end in self.rowPairs:  # 遍历存储了行的起始和结束位置的元组列表self.rowPairs。
            for j in range(self.len_y):  # 遍历二维数组的每一列
                if not self.data[start:end, j].all() and start_j < 0:  # 当前列的像素值不全为真（非白色像素）并且之前没有开始记录列的起始位置
                    start_j = j  # 将当前列的索引存储在start_j中。
                elif not self.data[start:end, j].all():  # 如果当前列的像素值不全为真（非白色像素），并且之前已经开始记录列的起始位置
                    end_j = j  # 将当前列的索引存储在end_j中。
                elif self.data[start:end, j].all() and start_j >= 0:
                    # 如果当前列的像素值全为真（全为白色像素），并且之前已经开始记录列的起始位置，则表示检测到了一个列的结束位置。
                    if end_j - start_j >= min_val:  # 如果检测到的列的长度大于等于min_val，则表示这是一个有效的列。
                        tmp = self.data[start:end, start_j:end_j]  # 据起始和结束位置的列索引，从原始二维数组中提取出这一列的图像。
                        tmp = cv2.copyMakeBorder(tmp, 10, 10, 10, 10, cv2.BORDER_CONSTANT,
                                                 value=[255, 255, 255])  # 给提取得到的图像添加边框。
                        tmp = cv2.resize(tmp, (self.dsize_x, self.dsize_y))  # 调整图像的大小。
                        cv2.imwrite(self.dividePath + '%d.png' % num, tmp)  # 将图像保存到本地文件中，使用num生成图像的文件名。
                        num += 1  # 增加计数器num的值。
                    start_j = -1
                    end_j = -1
        return num  # 返回保存的图像数量。


if __name__ == '__main__':
    divide = MyDivide('test12-1-pos.png')
    divide.Bgr2Gray()
    divide.Gray2Binary()
    divide.Binary2Array()
    divide.lineSeg()
    print(divide.rowPairs)
    print('分割成了',divide.columnSeg(),'张图片')
    cv2.imshow('g',divide.binary)
    cv2.waitKey(0)