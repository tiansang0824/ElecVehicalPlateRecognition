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


def make_user(result: tuple) -> User:
    g = Gender.MALE if result[2] == "M" else Gender.FEMALE
    return User(result[0], result[1], g, result[3], result[4], result[5])


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

    u = User(uname='田桑', gender=Gender.MALE, org="自软", phone='15703417063', email="zhanghaotian0824@qq.com")
    con.add_user(u)
