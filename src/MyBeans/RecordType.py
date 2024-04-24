from enum import Enum


class RecordType(Enum):
    """
    该类用于定义记录类型
    """
    ADD_USER = 101  # 添加用户信息
    ADD_PLATE = 102  # 添加车牌信息
    ADD_RELATION = 103  # 添加关系信息
    QUICK_ADD = 104  # 快速添加功能

    CHECK_USER = 201  # 搜索用户信息
    CHECK_PLATE = 202  # 搜索车牌信息

    DEL_USER = 301  # 删除用户信息
    DEL_PLATE = 302  # 删除车牌信息
    DEL_RELATION = 303  # 删除关系信息
