from enum import Enum


class RecordType(Enum):
    """
    该类用于定义记录类型
    """
    ADD_USER = "添加用户信息"  # 添加用户信息
    ADD_PLATE = "添加车牌信息"  # 添加车牌信息
    ADD_RELATION = "添加关系信息"  # 添加关系信息
    QUICK_ADD = "快速添加功能"  # 快速添加功能

    CHECK_USER = "搜索用户信息"  # 搜索用户信息
    CHECK_PLATE = "搜索车牌信息"  # 搜索车牌信息

    DEL_USER = "删除用户信息"  # 删除用户信息
    DEL_PLATE = "删除车牌信息"  # 删除车牌信息
    DEL_RELATION = "删除关系信息"  # 删除关系信息

    IDENTIFY = "识别车牌信息"


if __name__ == '__main__':
    print(RecordType.ADD_USER.value)
