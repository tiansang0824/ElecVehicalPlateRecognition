"""
Interface 类，该类用于提供统一的功能操作接口，规范化和统一化各个模块功能。
Interface 类，用于存储GUI界面操作中需要使用到的所有内容。
GUI 界面的每个功能都对应 interface 中的一个函数，通过一对一调用函数来直接实现 GUI 的功能。
"""
from src.MyBeans import User, Gender, Relation, Plate
from src.function import Position, Divide, Match
import src.base.DBConnector as db
import matplotlib as plt
import cv2


class Interface:
    file_path: str = None  # 原始图片路径
    file_name: str = None  # 原始图片名
    slice_path: str = None  # 字符切片路径

    unit_position = None  # 保存一个车牌定位实例
    unit_divide = None  # 保存一个字符分割实例
    unit_match = None  # 保存一个字符匹配实例
    unit_dbcon = None  # 保存一个数据库连接模组实例

    def __init__(self):
        """
        创建接口构造器
        注意，考虑到模块Position在创建的时候，构造器需要传入原始图片地址，
        但是在创建统一接口的时候无法传入对应地址，所以取消在构造器中创建实例的想法。
        """
        self.unit_dbcon = db.DBConnector(
            host="localhost",
            port=3306,
            user="root",
            password="root",
            database="db_pr"
        )

    def interface_login(self, username: str, password: str) -> bool:
        """
        该函数用于判断是否可以通过登录功能判断
        :param username:
        :param password:
        :return:
        """
        # 调用数据库模组检查是否存在该用户
        if_exists = self.unit_dbcon.select_admin_exist(username, password)
        if if_exists:  # 用户存在，通过检查
            return True
        else:  # 用户不存在，不通过检查
            return False

    def interface_select_master_by_plate(self, plate_num: str) -> User.User:
        """
        通过车牌号查找车主信息
        :param plate_num:
        :return:
        """
        select_result = self.unit_dbcon.select_user_by_pnum(plate_num)
        print(select_result)
        return select_result

    def insert_user(self, user_info: User):
        ret_uid = self.unit_dbcon.add_user(user_info)
        return ret_uid

    def insert_plate(self, plate_info: Plate):
        self.unit_dbcon.add_plate(plate_info)

    def insert_insert_plate(self, plate_num: str, remark: str) -> None:
        """
        添加新的车牌信息
        :param plate_num:
        :param remark:
        :return:
        """
        p = Plate.Plate(plate_num, remark)
        self.unit_dbcon.add_plate(p)

    def insert_relation(self, uid, pid):
        """
        添加关系信息函数
        :param uid:
        :param pid:
        :return:
        """
        self.unit_dbcon.add_relation(uid, pid)

    def select_userinfo(self, uid: str) -> User:
        return self.unit_dbcon.select_user_by_uid(uid)

    def select_plate_info(self, pid: str) -> Plate:
        return self.unit_dbcon.select_plate_by_pid(pid)

    def quick_add_relation(self, user_info: User, plate_info: Plate) -> tuple:
        """
        该函数用于快速添加用户信息、车牌信息，以及人车关系（用户信息、车牌信息和人车关系都是新添加的）
        :return:
            0: 添加成功
            1: 用户已存在
            2: 车牌已存在
        """
        # 测试代码：
        print("test code >> 开始执行函数：Interface.quick_add_relation")
        # 提前判断被添加的用户是否存在
        user_exists = self.unit_dbcon.check_user_exists(user_info)
        if user_exists:  # 用户存在
            return 1
        # 然后判断被添加的车牌信息是否存在
        plate_exists = self.unit_dbcon.check_plate_exists(plate_info)
        if plate_exists:  # 车牌信息存在
            return 2
        # 用户、车牌信息之前都不存在，那么显然人车关系也不存在
        # 这种情况下就可以正常添加人车关系信息
        # 添加用户信息
        uid = self.unit_dbcon.add_user(user_info)
        # 添加车牌信息
        pid = self.unit_dbcon.add_plate(plate_info)
        # 添加人车关系
        rid = self.unit_dbcon.add_relation(uid, pid)
        # 返回uid、pid、rid
        return (uid, pid, rid)

    def interface_identify(self, file_path: str):
        """
        该函数用于调用完整的图像识别模块，实现一键识别图片内容。
        @:param file_path: 原始图像位置
        :return:
        """
        # 第一步判断输入合法性
        if file_path is None:  # 判断输入内容是否为空
            return None  # 输入内容为空，终止函数，返回None
        # 接下来开始正式进行图片识别
        # 第一步：进行车牌定位
        plt.rcParams['font.family'] = ['Simsun']  # 修改plt字体
        # 创建定位模块
        self.unit_position = Position.MyPosition(file_path)
        # 去噪处理
        self.unit_position.remove_noise(self.unit_position.img)
        # 找到车牌位置
        img = self.unit_position.get_profile()
        # 输出处理过程
        self.unit_position.get_details()  # 过程测试代码
        # 展示图片
        cv2.imshow("plate area after process 1", img)
        cv2.waitKey()  # 避免cv展示图片闪退
        # 旋转车牌区域图片
        img = self.unit_position.Rotate()
        # 车牌图片去噪声
        self.unit_position.remove_noise(img)
        # 新图片重新获取车牌区域
        img = self.unit_position.get_profile()
        # 输出处理过程
        self.unit_position.get_details()  # 过程测试代码
        # 展示图片  # 过程测试代码
        cv2.imshow("plate area after process 2", img)
        cv2.waitKey()
        cv2.destroyAllWindows()
        # 保存图片
        self.unit_position.save()
        # 接下来做字符分割
        # 为了对接字符分割模组，需要获取到保存的文件的文件名，并且这个文件名不能够具有后缀名
        plate_area_file_name = self.unit_position.positionName[:-8]  # 获取文件名
        print(f"test code: 保存的车牌区域文件名为：{plate_area_file_name}")
        # 现在可以进行字符分割了
        # 创建字符分割单元
        self.unit_divide = Divide.MyDivide(plate_area_file_name)
        self.unit_divide.bgr2gray()
        self.unit_divide.gray2binary()
        self.unit_divide.binary2array()
        self.unit_divide.line_seg()
        self.unit_divide.col_seg()
        # 最后一步进行字符模板匹配
        # 先获取单字符图片位置
        # 合成保存路径
        save_path = self.unit_divide.dividePath
        print(f"test code: char image save path is {save_path}")  # 单字符保存位置测试成功。
        # 创建匹配模组实例
        self.unit_match = Match.Matcher(save_path)
        self.unit_match.match_all()
        final_answer = self.unit_match.get_final_answer()
        print(f"test code: final match answer is {final_answer}")
        # 调用结束，返回关键信息
        answer_list = list()
        answer_list.append(self.unit_position.positionPath + self.unit_position.positionName)  # 第一个是车牌区域的缓存图片地址
        answer_list.append(final_answer)  # 第二个是车牌识别的最终结果
        print(answer_list)  # 打印结果进行测验
        return answer_list  # 返回结果


if __name__ == '__main__':
    print("this is Interface test demo.")
    i = Interface()
    user = i.interface_select_master_by_plate("123abc")
    print(user.phone)
