/*

创建一个MySQL数据库，叫做db_pr，然后执行下面的全部代码即可再现数据库。

该文件中保存的是对数据库db_pr的全部操作语句。

该数据库中主要存储电动车信息和车主信息两张表格，通过外键连接。
@t_user: 该表格存储用户（学生）信息。
@t_plate: 该表格存储车牌信息。
@t_relation: 该表保存用户和电动车关联信息。

*/

# 选中数据库
use db_pr;

# 删除全部表格
drop table t_relation;
drop table t_user;
drop table t_plate;
drop table t_admin;
drop table t_record;

# 创建管理员表
CREATE TABLE `t_admin` (
  `username` varchar(12) NOT NULL,
  `password` varchar(12) NOT NULL,
  PRIMARY KEY (`username`)
);

# 创建用户表
create table if not exists t_user
(
    uid    int auto_increment,
    uname  varchar(32)     not null,
    gender enum ('M', 'F') not null comment '保存性别信息',
    org    varchar(128)    not null comment '保存用户所属班级等信息',
    phone  varchar(16)     not null comment '保存用户联系电话号',
    email  varchar(32)     not null comment '保存用户邮箱信息',
    constraint t_user_pk_uid primary key (uid)
);

# 创建车牌表
create table if not exists t_plate
(
    pid    int auto_increment,
    pnum   varchar(8) not null unique comment '车牌号',
    remark varchar(255) comment '备注信息',
    primary key (pid)
);

# 创建关系表
create table if not exists t_relation
(
    rid    int auto_increment comment '关联关系主键',
    uid    int not null comment '外键，连接用户id',
    pid    int not null comment '外键，连接车牌id',
    remark varchar(128) comment '备注信息',
    primary key (rid),
    foreign key (uid) references t_user (uid),
    foreign key (pid) references t_plate (pid)
);

/* 下面是插入数据 */
# 插入管理员表数据
insert into t_admin(username, password)
values('admin', '123456');


/* 插入用户数据 */
insert into t_user(uid, uname, gender, org, phone, email)
values (10000, '田桑', 'M', '自动化与软件学院', '15703417063', 'tiansang@163.com'),
       (10001, '蓉酱', 'F', '自动化与软件学院', '19581540753', 'rongjiang@qq.com');


/* 虚拟用户数据 */
INSERT INTO t_user (uname, gender, org, phone, email)
VALUES ('吴九', 'M', '自动化与软件学院', '17705415719', 'hcoziwma@126.com'),
       ('叶璐', 'M', '计算机与信息技术学院', '13459726858', 'ymydwgij@qq.com'),
       ('丁欣怡', 'M', '哲学院', '13405337130', 'kvpvtvpc@outlook.com'),
       ('谢瑾昆', 'F', '电力与建筑学院', '18686007731', 'djybuctg@126.com'),
       ('崔国贤', 'M', '物理学院', '13964979872', 'yfveaadf@qq.com'),
       ('李岚', 'M', '商学院', '18431197873', 'zanuwmii@126.com'),
       ('姜晓明', 'F', '计算机与信息技术学院', '13579332978', 'pypxakmr@126.com'),
       ('熊云熙', 'F', '哲学院', '13925819016', 'ypznzgav@163.com'),
       ('夜戮', 'F', '自动化与软件学院', '18733708403', 'yuagsmbn@qq.com'),
       ('布史东', 'M', '电力与建筑学院', '18948079406', 'beeujaia@163.com'),
       ('王五', 'F', '哲学院', '13987931155', 'hjihqwlq@qq.com'),
       ('赵六', 'F', '计算机与信息技术学院', '13832164064', 'yqnufkav@qq.com'),
       ('孙七', 'M', '自动化与软件学院', '18694041754', 'ygcfavae@126.com'),
       ('周八', 'M', '商学院', '15344452978', 'kocwpwrd@qq.com'),
       ('汪晓明', 'M', '电力与建筑学院', '15267866104', 'iygooons@qq.com'),
       ('陆致远', 'M', '自动化与软件学院', '18943922185', 'uuwindsu@qq.com'),
       ('严子韬', 'M', '计算机与信息技术学院', '15868050851', 'thvgefqa@126.com'),
       ('高秀英', 'F', '电力与建筑学院', '15809076788', 'wgosplrj@qq.com'),
       ('李子异', 'F', '哲学院', '13768568072', 'dnfyjpvg@126.com'),
       ('陶宇宁', 'F', '商学院', '15637912883', 'pebdxolr@qq.com'),
       ('袁璐', 'F', '自动化与软件学院', '15125213849', 'bihpmmyy@126.com'),
       ('朱詩涵', 'F', '计算机与信息技术学院', '13623184196', 'ulppeoud@qq.com'),
       ('吕睿', 'F', '哲学院', '13152009641', 'fswnreul@126.com'),
       ('林安琪', 'M', '商学院', '13939008164', 'buqzflcn@126.com'),
       ('任宇宁', 'M', '哲学院', '15257536258', 'hcvugqtu@qq.com'),
       ('徐杰宏', 'F', '自动化与软件学院', '13501469190', 'nqmqbenw@163.com'),
       ('姜杰宏', 'F', '计算机与信息技术学院', '15190194108', 'zmcplleq@163.com'),
       ('冯安琪', 'M', '电力与建筑学院', '18110108899', 'hmkmxxfm@outlook.com');

/* 插入车牌数据 */
insert into t_plate(pid, pnum, remark)
values (20000, 'M28199', '备注信息，车牌默认六位字符'), (20001, '143075', '备注信息，用于测试');

# 插入随机数据
insert into t_plate(pnum, remark)
values ('L58720', '不含有大写字母I和O'),
       ('J35130', ''),
       ('L65783', ''),
       ('L83156', ''),
       ('223648', ''),
       ('L65765', ''),
       ('L99859', ''),
       ('292256', '');

/* 插入关系数据 */
insert into t_relation(rid, uid, pid, remark)
values (30000, 10000, 20000, '测试数据');

# 插入假关系
insert into t_relation(uid, pid)
values (10001, 20001);
insert into t_relation(uid, pid)
values (10002, 20002);
insert into t_relation(uid, pid)
values (10003, 20003);

# 添加记录表
create table t_record(
    record_id int auto_increment,
    operator varchar(16),
    record_type varchar(32),
    backup varchar(64),
    op_date DATETIME,
    primary key(record_id)
    );

# 测试一个记录
insert into t_record values(90001, 'admin', '添加新用户', '测试备注信息', now());