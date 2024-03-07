"""
数据库连接模块
该模块负责直接连接数据库，实现对数据库数据的增删改查操作
"""
from pymysql import Connection


class DBConnector:
    # 被链接数据库信息
    host = ''
    port = 0000
    user = ''
    password = ''
    db_name = ''
    # 内置对象
    conn = None
    cursor = None

    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db_name = database

    def select_user(self):
        pass

    def select_plate(self):
        pass

    def select_relation(self):
        pass

    def add_user(self):
        pass

    def add_plate(self):
        pass

    def add_relation(self):
        pass

    def delete_user(self):
        pass

    def delete_plate(self):
        pass

    def delete_relation(self):
        pass

    def update_user(self):
        pass

    def update_plate(self):
        pass

    def update_relation(self):
        pass


if __name__ == '__main__':
    print('数据库操作模块测试代码：')
