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
from src.MyBeans.RecordType import RecordType
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

    def add_record(self, admin_username: str, record_type: RecordType, backup: str)->bool:
        """
        用于向记录表中添加操作记录
        :param admin_username: 操作者的用户名
        :param record_type: 记录操作类型
        :param backup: 记录附注信息，这个信息应该来自上一层，这里只要如实传入即可。
        :return:
        """
        print(f">> DBConnector层级：打印记录类型：{record_type.value}")
        try:
            sql = (f"insert into t_record(operator, record_type, backup, op_date) "
                   f"values('{admin_username}', '{record_type.value}', '{backup}', now());")
            self._cursor.execute(sql)  # 执行备注
            self._conn.commit()  # 提交事务
            print(">> 记录信息添加完成")
            return True
        except Exception as e:
            print(">> 记录信息添加失败")
            return False

    def select_records(self):
        """
        该函数用于搜索和返回数据库操作记录
        :return:
        """
        sql = f"select * from t_record order by op_date desc"
        self._cursor.execute(sql)
        result = self._cursor.fetchall()
        print(result)
        return result

    def select_user_by_phone(self, phone):
        sql = f"select * from t_user where phone = '{phone}'"
        self._cursor.execute(sql)
        result = self._cursor.fetchall()[0]
        return make_user(result)

    def select_user_by_pnum(self, plate_num):
        sql = (f"select u.* "
               f"from t_plate p left join t_relation r on r.pid = p.pid left join t_user u on r.uid = u.uid "
               f"where p.pnum = '{plate_num}'")
        self._cursor.execute(sql)
        result = self._cursor.fetchall()[0]
        return make_user(result)

    def select_user_by_uid(self, uid):
        sql = f"select u.* from t_user u where uid = '{uid}'"
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

    def select_plate_by_pid(self, pid: str):
        """通过pid搜索车牌信息"""
        sql = f"select p.* from t_plate p where p.pid = {pid}"
        self._cursor.execute(sql)
        result = self._cursor.fetchall()[0]
        # print(f"test code >> 车牌搜索结果为：{result[0]},{result[1]},{result[2]}")
        return Plate(pid=result[0], pnum=result[1], remark=result[2])

    def check_user_exists(self, user: User):
        """
        通过用户的所有非主属性组合，判断用户是否存在
        :param user:
        :return:
        """
        uname = user.uname
        gender = "F" if user.gender == Gender.FEMALE else "M"
        phone = user.phone
        email = user.email
        sql = (f"select u.* from t_user u where u.uname='{uname}' and u.gender='{gender}' "
               f"and u.phone='{phone}' and u.email='{email}';")  # 写好sql
        self._cursor.execute(sql)
        result = self._cursor.fetchall()
        if len(result) == 0:
            # 说明没有查到东西，目标用户不存在
            return False
        else:
            # 查到了内容，目标用户存在
            return True

    def check_plate_exists(self, plate: Plate):
        pnum = plate.pnum
        sql = f"select p.* from t_plate p where p.pnum = '{pnum}'"
        self._cursor.execute(sql)
        result = self._cursor.fetchall()
        if len(result) == 0:
            # 说明没有查到东西，目标车牌不存在
            return False
        else:
            # 查到了内容，目标车牌存在
            return True

    def check_admin_exists(self, username: str) -> bool:
        sql = f"select a.* from t_admin a where a.username='{username}';"
        self._cursor.execute(sql)
        result = self._cursor.fetchall()
        if len(result) == 0:
            return False
        else:
            return True

    def add_admin(self, admin_info: list) -> bool:
        sql = f"insert into t_admin values('{admin_info[0]}', '{admin_info[1]}')"
        try:
            self._cursor.execute(sql)
            self._conn.commit()
            return True
        except Exception as e:
            return False

    def add_user(self, user_info: User) -> int:
        """
        添加用户信息，返回新用户uid
        :param user_info:
        :return:
        """
        g = "M" if user_info.gender == Gender.MALE else "F"
        sql = (f"insert into t_user(uname, gender, org, phone, email) "
               f"values('{user_info.uname}', '{g}', '{user_info.org}', '{user_info.phone}', '{user_info.email}')")
        # print(sql)
        self._cursor.execute(sql)
        self._conn.commit()  # 提交修改
        # select操作与事务无关，故提前提交事务
        # 接下来找到新用户的uid，将其返回给调用者
        sql_select = (f"select u.uid from t_user u "
                      f"where uname = '{user_info.uname}' and gender= '{g}' and org = '{user_info.org}'"
                      f"and phone = '{user_info.phone}' and email = '{user_info.email}'")
        self._cursor.execute(sql_select)
        result = self._cursor.fetchall()[0][0]
        print(f"test code >> DBConntor添加用户函数返回的用户uid搜索结果：{result}")
        print('用户信息添加完毕')
        return result

    def add_plate(self, plate_info: Plate):
        sql = f"insert into t_plate(pnum, remark) values('{plate_info.pnum}', '{plate_info.remark}')"
        self._cursor.execute(sql)
        self._conn.commit()
        # 接下来搜索一次车牌信息
        sql_select = (f"select p.pid from t_plate p "
                      f"where p.pnum = '{plate_info.pnum}' and p.remark = '{plate_info.remark}';")
        self._cursor.execute(sql_select)
        result = self._cursor.fetchall()[0][0]
        print(f"test code >> 搜索车牌pid结果：{result}")
        print('车牌信息添加完毕')
        return result

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
        sql_select = f"select r.rid from t_relation r where r.uid = {uid} and r.pid = {pid};"
        self._cursor.execute(sql_select)
        result = self._cursor.fetchall()[0][0]
        print('人车信息添加完毕')
        return result

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
    """
    u = con.select_user_by_phone("18686007731")
    print(f'通过电话号查找车主信息：{u.uname, u.gender, u.org, u.phone, u.email}', end='\n\n')
    # u = con.select_user_by_pnum('123abc')
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
    # 测试通过pid搜索车牌信息
    ret = con.select_plate_by_pid("20001")
    print(f"test code >> 通过pid搜索车牌信息：{ret}")

    # 测试检查用户和车牌是否存在的函数是否可用
    # 首先创建用户
    u = User("田桑", Gender.FEMALE, "用户信息演示", "15703417063", "tiansang@163.com")
    # 检查用户是否存在
    print(f'存在性：{con.check_user_exists(u)}')
    # 创建车牌信息
    p = Plate("M28199", "备注信息，车牌默认六位字符")
    print(f'车牌信息存在性：{con.check_plate_exists(p)}')
    # 测试添加函数是否返回id
    u = User("tiantiantiantian", Gender.FEMALE, "wok", "15703417066", "tiansang111@163.com")
    print(f"{con.add_user(u)}")
    # 创建车牌信息
    p = Plate("XYZ123", "测试信息")
    print(f"添加车牌返回值：{con.add_plate(p)}")
    # 测试添加关系的函数是否返回rid
    print(f"测试添加关系函数的返回值：{con.add_relation(10030, 20010)}")
    print(f"测试添加关系函数的返回值：{con.add_relation(10021, 20009)}")
    
        """

    con.add_record("admin", record_type=RecordType.ADD_RELATION, backup="测试内容")
    records = con.select_records()
    for record in records:
        print(record[4])