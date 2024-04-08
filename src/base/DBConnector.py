"""
数据库连接模块
该模块负责直接连接数据库，实现对数据库数据的增删改查操作

添加信息：
- 添加用户信息；
- 添加电动车信息；
- 添加人车关系；

删除信息：
- 删除用户信息；
- 删除电动车信息；
- 删除人车关系；

修改信息：
- 修改用户信息；
- 修改电动车信息；
- 修改人车关系信息；

查询信息：
- (x) 通过id查询车主信息；
- 通过电话号查询车主信息；
- 通过车牌号查询车主信息；
- (x) 通过id查询车牌信息；
- 通过车主电话号查询车牌信息；

"""
from pymysql import Connection
from src.MyBeans.Gender import Gender
from src.MyBeans.User import User
from src.MyBeans.Plate import Plate
from src.MyBeans.Relation import Relation


def make_user(result: tuple) -> User:
    g = Gender.MALE if result[2] == "M" else Gender.FEMALE
    return User(result[1], g, result[3], result[4], result[5], uid=result[0])


def make_plate(result: tuple) -> Plate:
    return Plate(result[0], result[1], result[2])


class DBConnector:
    _host = None
    _port = None
    _user = None
    _password = None
    _database = None

    _conn = None
    _cursor = None

    def __init__(self, host, port, user, password, database):
        self._host = host
        self._port = port
        self._user = user
        self._password = password
        self._database = database

        self._conn = Connection(
            host=host,
            port=port,
            user=user,
            passwd=password,
            database=database
        )
        self._cursor = self._conn.cursor()

    def select_user_by_phone(self, phone):
        sql = f"select * from t_user where phone = '{phone}'"
        self._cursor.execute(sql)
        result = self._cursor.fetchall()[0]
        return make_user(result)

    def select_user_by_pnum(self, email):
        sql = (f"select u.* "
               f"from t_plate p left join t_relation r on r.pid = p.pid left join t_user u on r.uid = u.uid "
               f"where p.pnum = '123abc'")
        self._cursor.execute(sql)
        result = self._cursor.fetchall()[0]
        return make_user(result)

    def select_plate_by_user_phone(self, phone):
        sql = (f"select p.* "
               f"from t_user u left join t_relation r on u.uid = r.uid left join t_plate p on r.pid = p.pid "
               f"where u.phone = '{phone}'")
        self._cursor.execute(sql)
        result = self._cursor.fetchall()[0]
        # print(f'result: {result}')
        return make_plate(result)

    def add_user(self, user_info: User):
        g = "M" if user_info.gender == Gender.MALE else "F"
        sql = (f"insert into t_user(uname, gender, org, phone, email) "
               f"values('{user_info.uname}', '{g}', '{user_info.org}', '{user_info.phone}', '{user_info.email}')")
        # print(sql)
        self._cursor.execute(sql)
        self._conn.commit()
        print('用户信息添加完毕')

    def add_plate(self, plate_info: Plate):
        sql = f"insert into t_plate(pnum, remark) values('{plate_info.pnum}', '{plate_info.remark}')"
        self._cursor.execute(sql)
        self._conn.commit()
        print('车牌信息添加完毕')

    def add_relation(self, uid: int, pid: int):
        """
        添加人车关系的函数。
        该函数的主要流程如下：

        :param uid:
        :param pid:
        :return:
        """
        sql = f"insert into t_relation(uid, pid) values ({uid}, {pid});"
        self._cursor.execute(sql)
        self._conn.commit()
        print('人车信息添加完毕')

    def del_user_by_id(self, uid: int):
        """
        通过用户id删除用户信息
        :param uid:
        :param user_id:
        :return:
        """
        sql = f"delete from t_user where uid = {uid};"
        self._cursor.execute(sql)
        self._conn.commit()
        print("用户信息删除完毕")

    def del_plate_by_pid(self, pid: int):
        sql = f"delete from t_plate where pid = {pid};"
        self._cursor.execute(sql)
        self._conn.commit()
        print("车牌信息删除完毕")

    def del_relation_by_id(self, rid):
        sql = f"delete from t_relation where rid = {rid};"
        self._cursor.execute(sql)
        self._conn.commit()
        print("关系信息删除完毕")

    def update_user_info(self, user_info: User):
        """
        修改用户信息
        :param user_info:
        :return:
        """
        # 获取信息
        [uid, uname, gender, org, phone, email] = (
            user_info.uid, user_info.uname, user_info.gender, user_info.org, user_info.phone, user_info.email)
        gender = "M" if gender == Gender.MALE else "F"
        # 创建sql语句
        sql = (f"update t_user set uname='{uname}', gender='{gender}', org='{org}', phone='{phone}', email='{email}' "
               f"where uid = {uid};")
        self._cursor.execute(sql)
        self._conn.commit()
        print("用户信息更新成功")

    def update_relation_info(self, relation_info: Relation):
        rid = relation_info.rid
        uid = relation_info.uid
        pid = relation_info.pid
        # print(f'rid={rid}, uid={uid}, pid={pid}')
        sql = f"update t_relation set uid={uid}, pid={pid} where rid={rid};"
        self._cursor.execute(sql)
        self._conn.commit()
        print("更新关系信息完毕")

    def select_admin_exist(self, admin_name: str, admin_pwd: str) -> bool:
        """
        该函数用于检查指定管理员用户是否存在
        @param admin_name: 管理员名
        @param admin_pwd: 管理员密码
        :return: 存在，返回True，否则返回False
        """
        sql = f"select * from t_admin where username = '{admin_name}' and password = '{admin_pwd}';"
        self._cursor.execute(sql)
        result = self._cursor.fetchall()
        print(f"搜索管理员用户的结果：{result}")
        if len(result) == 0:
            return False
        else:
            return True


if __name__ == '__main__':
    con = DBConnector(
        host="localhost",
        port=3306,
        user="root",
        password="root",
        database="db_pr"
    )
    u = con.select_user_by_phone("18686007731")
    print(f'通过电话号查找车主信息：{u.uname, u.gender, u.org, u.phone, u.email}', end='\n\n')
    u = con.select_user_by_pnum('123abc')
    print(f'通过车牌号查找车主信息：{u.uname, u.gender, u.org, u.phone, u.email}', end='\n\n')
    p = con.select_plate_by_user_phone('15703417063')
    print(f'通过电话号查找车牌信息：{p.pnum, p.remark}')
    # 添加用户测试
    u = User(uname='田桑', gender=Gender.MALE, org="自软", phone='15703417063', email="zhanghaotian0824@qq.com")
    con.add_user(u)
    # 添加车牌信息测试
    p = Plate('qwerty', '测试用的remark字段')
    con.add_plate(p)
    # 添加关系测试
    con.add_relation(10007, 20007)
    # 删除用户测试
    con.del_user_by_id(10026)
    # 更新用户信息
    u = User("姜子牙", Gender.FEMALE, "封神榜", '12345674567', 'ziya@163.com', uid=10007)
    con.update_user_info(u)
    # 更新关系信息
    r = Relation(30006, 10006, 20009)
    con.update_relation_info(r)
    # 搜索管理员用户
    print(f"管理员搜索结果为：{con.select_admin_exist('admin', 'root')}")
