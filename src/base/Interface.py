"""
Interface 类，该类用于提供统一的功能操作接口，规范化和统一化各个模块功能。

Interface 类，用于存储GUI界面操作中需要使用到的所有内容。

GUI 界面的每个功能都对应 interface 中的一个函数，通过一对一调用函数来直接实现 GUI 的功能。

GUI 功能列表：
- 传入图片
- 车牌处理
- 字符分割
- 文字识别
- 通过车牌识别结果 查询对应用户
- 通过车牌识别结果 添加用户绑定
- 修改用户信息
- 修改车牌信息
- 修改绑定关系

"""
from src.MyBeans import *


class Interface:
    pass


if __name__ == '__main__':
    pass
