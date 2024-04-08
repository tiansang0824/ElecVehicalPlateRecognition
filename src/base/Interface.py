"""
Interface 类，该类用于提供统一的功能操作接口，规范化和统一化各个模块功能。
Interface 类，用于存储GUI界面操作中需要使用到的所有内容。
GUI 界面的每个功能都对应 interface 中的一个函数，通过一对一调用函数来直接实现 GUI 的功能。
"""
from src.MyBeans import *
from src.function import Position, Divide, Match
import src.base.DBConnector as db


class Interface:
    file_path: str = None  # 原始图片路径
    file_name: str = None  # 原始图片名
    slice_path: str = None  # 字符切片路径

    model_position = None  # 保存一个车牌定位实例
    model_divide = None  # 保存一个字符分割实例
    model_match = None  # 保存一个字符匹配实例
    model_dbcon = None  # 保存一个数据库连接模组实例

    def __init__(self):
        """
        创建接口构造器
        注意，考虑到模块Position在创建的时候，构造器需要传入原始图片地址，
        但是在创建统一接口的时候无法传入对应地址，所以取消在构造器中创建实例的想法。
        """
        self.model_dbcon = db.DBConnector(
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
        if_exists = self.model_dbcon.select_admin_exist(username, password)
        if if_exists:  # 用户存在，通过检查
            return True
        else:  # 用户不存在，不通过检查
            return False


if __name__ == '__main__':
    print("this is Interface test demo.")
