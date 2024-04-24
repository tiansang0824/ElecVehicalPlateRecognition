# 导入所需模块
import cv2
import numpy as np
from matplotlib import pyplot as plt
import os


class MyDivide(object):
    imgName = ''  # 保存图片名
    imgPath = 'D:/cache/position/'  # 图片路径
    dividePath = 'D:/cache/divide/'  # 分割图片的保存位置

    img = []
    gray = []  # 用于保存灰度图
    binary = []  # 用于保存二值图
    data = []  # 用于以数组的形式保存图片
    len_x = []  # x方向长度
    len_y = []  # y方向长度
    row_pairs = []  # 竖直方向切割后包含字符的行信息集合
    col_pairs = []  # 水平方向切割后包含字符的列信息集合

    rows = []  # 行数
    cols = []  # 列数

    # 下面的属性主要用于竖直方向切割的时候用。
    min_val = 15  # 最小密度，用于筛除较大的噪点

    #

    def __init__(self, name):
        self.imgName = name  # 读取图片名
        self.dividePath = self.dividePath + name.split('-', 1)[0] + '/'  # 设置保存路径（和文件名）
        self.img = cv2.imread(self.imgPath + self.imgName + '-pos.png')  # 到指定文件夹读取文件（定位后的车牌区域图片）

        x = self.img.shape[0]  # 获取图片rows
        y = self.img.shape[1]  # 获取图片cols
        self.row_pairs = []  # 原始变量名是 rowPairs

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
        # cv2.imshow('original image', self.img)
        # cv2.waitKey(0)

    def bgr2gray(self):
        """
        原始图片转换成灰度图
        :return:
        """
        self.gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)

        # cv2.imshow('gray image', self.gray)  # 测试代码，输出灰度图
        # cv2.waitKey(0)  # waitKey

        return self.gray

    def gray2binary(self):
        """
        灰度图转换成二值图
        :return:
        """

        average_gray = np.mean(self.gray)
        ret, self.binary = cv2.threshold(self.gray, average_gray, 255, cv2.THRESH_BINARY_INV)

        # ret, self.binary = cv2.threshold(self.gray, 127, 255, cv2.THRESH_BINARY_INV)

        # cv2.imshow('binary image', self.binary)  # 测试代码：输出二值图
        # cv2.waitKey(0)  # waitKey

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

        # print(f'data: {self.data}')  # 测试代码，输出转化后的数组
        # print(f'len_x: {self.len_x}, len_y: {self.len_y}')  # 测试代码，输出数组的长宽

        return self.data

    def line_seg(self):
        """
        函数lineSeg, 从二维数组中检测线段的起始和结束位置，并将这些位置存储在row_pairs列表中。
        :return:
        """
        # 初始化变量start_i和end_i，它们用于存储线段的起始和结束位置的行索引。
        start_i = -1
        end_i = -1
        # 初始化空列表row_pairs，用于存储检测到的线段的起始和结束位置的行索引对。
        self.row_pairs = []

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
                    self.row_pairs.append((start_i, end_i))  # 如果大于最小高度，则视作是字符段，追加到self.row_pairs中。
                start_i = -1  # 重置起始位置（行号）
                end_i = -1  # 重置结束位置（行号）

        print(f'self.row_pairs: {self.row_pairs}')  # 测试代码，输出截取到的字符区域（竖直方向）

    def col_seg(self):
        """
        该函数用于将切分后的含有车牌字符的行集合进行水平方向切分，从而将每个字符所在区域划分为单一的图片
        :return:
        """
        print('接下来进入col_seg()函数所在范围')  # 测试代码，标记代码执行进度
        # 首先检查self.row_pair是否只含有一个元素（是否准确查找到字符所在行集合）
        if len(self.row_pairs) > 1:
            # 垂直分割后得到不止一个集合
            # 只留下最大的集合
            max_row_len = 0  # 标记最大集合包含行数
            for segment in self.row_pairs:
                # 该轮循环用于查找到最大的row_len
                if segment[1] - segment[0] > max_row_len:
                    max_row_len = segment[1] - segment[0]  # 为最大row_len赋值
            for segment in self.row_pairs:
                # 第二轮循环，用于删除非最大的row_len所在集合
                if segment[1] - segment[0] < max_row_len:
                    self.row_pairs.remove(segment)  # 删除所在的segment
        # 然后从二值图截取self.row_pairs标记的行集合
        binary_copy = self.binary.copy()
        start_row = self.row_pairs[0][0]  # 起始行
        end_row = self.row_pairs[0][1]  # 结束行
        binary_copy = binary_copy[start_row:end_row, :]  # 获取垂直分割后的含有字符的行集合
        # cv2.imshow('binary_copy, contains string', binary_copy)
        # cv2.waitKey(0)
        """
        到这里为止，binary_copy就是只含有字符的行集合组成的图片。
        接下来裁剪每个字符所在的列
        列裁剪的大致步骤如下：
        1. 根据copy图片获得竖直方向的直方图；
        2. 处理直方图，去掉小噪点；
        -  注意：去除噪点后的直方图，分割后获取到的元素中，第一个和最后一个是是车牌框留下的黑色像素点，需要剔除掉
        3. 分割并获取列集合
        4. 剔除首尾车牌框的集合
        四个步骤结束后，接客完成字符分割
        """
        # 1. 获取直方图
        [rows, cols] = binary_copy.shape
        print(f'binary_copy.shape: {rows, cols}')  # 测试代码
        # 二值统计,统计每一列的黑值（0）的个数
        black_nums = []  # black_num 用于保存每一列上包含的黑色像素点个数
        for col in range(cols):
            res = 0
            for row in range(rows):
                if binary_copy[row][col] == 0:
                    res = res + 1
            black_nums.append(res)
        # len(black_nums)
        # max(black_nums)
        # 2. 筛选直方图
        black_sum = 0  # 黑色像素点加和
        one_fourth_point = int(sum(black_nums) / len(black_nums) / 4) + 1  # 三分之一点(+1是为了向上取整)
        print(f'三分之一点：{one_fourth_point}')  # 测试代码；直方图三分之一点
        # 简单筛选
        for i in range(cols):
            if black_nums[i] < one_fourth_point:
                black_nums[i] = 0
        # 画出柱状图
        y = black_nums  # 点个数
        x = [x for x in range(cols)]  # 列数
        plt.bar(x, y, color='black', width=1)
        # 设置x，y轴标签
        plt.xlabel('col')
        plt.ylabel('0_number')
        # 设置刻度
        plt.xticks([x for x in range(0, cols, 10)])
        plt.yticks([y for y in range(0, max(black_nums) + 5, 5)])
        plt.rcParams['font.sans-serif'] = ['SimHei']  # SimHei是黑体的意思
        # plt.rcParams['font.family'] = ''   # 中文不乱码
        plt.title('直方图')
        plt.show()
        # 3. 根据直方图获取每个单字符的列集合
        self.col_pairs = []  # 对列集合置空
        # 找所有不为0的区间(列数)
        reg = []
        for i in range(cols - 1):
            if black_nums[i] == 0 and black_nums[i + 1] != 0:
                # 该列为零，但是下一列不为零，这是区间的起始点：black_nums[i] == 0 and black_nums[i + 1] != 0
                # 该列不为零，但是前一列为零，那么前一列是起点
                reg.append(i)
            elif black_nums[i] != 0 and black_nums[i + 1] == 0:
                # 该列不为零但是下一列为零，这是区间的结束点：black_nums[i] != 0 and black_nums[i + 1] == 0：reg.append(i + 2)
                # 该列为零，但是前一列不为零，那么该列的下一列作结束点
                reg.append(i + 2)
            elif i == (cols - 2) and black_nums[i] != 0 and len(reg) == 1:
                # 最后一列
                reg.append(i)
                self.col_pairs.append(reg)
                reg = []
                break
            elif i == 0 and black_nums[i] != 0:
                # 第一列
                reg.append(i)
            if len(reg) == 2:
                # 判断是否记录了一个完整区间
                if (reg[1] - reg[0]) > 5:  # 限定区间长度要大于5(可以更大),过滤掉不需要的点
                    self.col_pairs.append(reg)
                    reg = []
                else:
                    reg = []
            print(f'reg: {reg}')  # 测试代码
        # 4. 剔除首尾车牌框位置
        self.col_pairs = self.col_pairs[1:-1]
        # 【不要整段删除】测试代码，输出测试车牌字符，顺便保存到本地目录内。
        for i in range(len(self.col_pairs)):
            # 当遇到数字1的时候，图片宽度过小，所以进行筛选和修正
            if (self.col_pairs[i][1] - self.col_pairs[i][0]) < 20:
                self.col_pairs[i][1] += 8
                self.col_pairs[i][0] -= 8
            # 从临时图片中裁剪字符区域
            tmp_image = self.img[self.row_pairs[0][0]:self.row_pairs[0][1],
                        self.col_pairs[i][0] - 1:self.col_pairs[i][1] + 1]
            # cv2.imshow(f'test_char: {i}', tmp_image)  # 测试代码
            # cv2.waitKey(0)  # 测试代码
            # 确保目标文件夹存在
            os.makedirs(self.dividePath, exist_ok=True)
            # 合成保存路径
            save_path = self.dividePath + f'{self.imgName}-{i}.jpg'
            print(f"char image save path: {save_path}")  # 输出测试图片保存位置
            # 保存图片
            cv2.imwrite(save_path, tmp_image)  # 保存字符图片
        # 5. 基本完成（下面是一个补充步骤，用于预备好字符串图片）
        tmp_image = self.binary[self.row_pairs[0][0] - 5:self.row_pairs[0][1] + 5,
                    self.col_pairs[0][0] - 2: self.col_pairs[len(self.col_pairs) - 1][1] + 2]
        """
        left_value = 0
        right_value = 0

        if self.col_pairs[0][0] - 2 <= 0:
            left_value = 0
        else:
            left_value = self.col_pairs[0][0] - 2

        if (self.col_pairs[len(self.col_pairs) - 1][1] + 2) >= self.binary.shape[1]:
            right_value = self.binary.shape[1]
        else:
            left_value = (self.col_pairs[len(self.col_pairs) - 1][1] + 2)

        tmp_image = self.binary[self.row_pairs[0][0] - 5:self.row_pairs[0][1] + 5, left_value: right_value]
        """
        # cv2.imshow('test: string area', tmp_image)
        # cv2.waitKey(0)
        # cv2.imwrite(self.dividePath + f'{self.imgName}-string.jpg', tmp_image)

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
        for pair in self.row_pairs:
            # pair表示每一个配对
            start_row = pair[0]
            end_row = pair[1]
            tmp_image = self.binary[start_row:end_row, :]
            cv2.imshow('tmp img', tmp_image)
            cv2.waitKey(0)


if __name__ == '__main__':
    md = MyDivide('test01')  # 通过图片名读取图片
    md.bgr2gray()  # 转换成灰度图
    md.gray2binary()  # 转换成二值图
    md.binary2array()  # 转换成数组
    md.line_seg()  # 切分字符位置
    # md.show_vertical_segment()  # 测试代码：输出竖直切分后的图片部分
    """
    line_seg()执行完毕后，self.row_pairs就保存了字符所在的行数，
    接下来就是对这个行的集合进行水平方向分割。
    """
    md.col_seg()
