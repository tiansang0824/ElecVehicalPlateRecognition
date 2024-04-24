import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename  # 用来获取用户文件路径
from PIL import ImageTk, Image  # 用来读取图片
import re
from tkinter import messagebox
from src.base.Interface import Interface
from src.MyBeans import User, Plate, Relation, Gender
from src.MyBeans.RecordType import RecordType


def make_user(result: tuple) -> User:
    g = Gender.Gender.MALE if result[2] == "M" else Gender.Gender.FEMALE
    return User.User(result[1], g, result[3], result[4], result[5], uid=result[0])


def make_plate(result: tuple) -> Plate:
    return Plate.Plate(result[0], result[1], result[2])


class Match:
    root = None  # 主窗口

    # 下面是左侧的组件
    left_frm = None  # 左侧内容框架
    left_title_label = None  # 左侧标题标签
    left_img_label = None  # 用于显示完整图片
    left_match_btn = None  # 一键读取车牌号
    left_details_btn = None  # 逐步读取车牌号
    # file_path = askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg")])
    # file_path = None  # 用于保存图片路径

    # 下面是右侧组件列表
    right_frm = None  # 右侧内容框架
    right_title_label = None  # 右侧标题标签
    right_img_label = None  # 显示右侧车牌所在图片
    right_remind_label = None
    right_plate_label = None  # 显示右侧车牌识别结果
    right_query_btn = None  # 查询车主信息按钮
    right_register_btn = None  # 等级车牌信息按钮

    # 其他变量
    file_path = None  # 用于保存图片路径
    photo_image = None

    admin_username: str = None  # 标记当前的登录者

    def __init__(self, master=None, admin_user=None):
        self.root = master
        self.admin_username = admin_user
        print(f">> 此时登录的管理员为：{self.admin_username}")
        self.root.title("车牌识别系统")
        self.root.geometry("860x500+100+100")
        self.root.resizable(False, False)
        self.var_plate_number = tk.StringVar()
        self.create_gui()

    def menu_import_file(self):
        """
        导入图片并且显示到左侧初始图片框中.
        :return:
        """
        # 暂时隐藏内容
        self.root.withdraw()
        # 弹出搜索框获取图片地址
        self.file_path = askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg")])

        if self.file_path:
            print(f"file path: {self.file_path}")
            try:
                photo = Image.open(self.file_path)
                photo = photo.resize((300, 300))  # 先调整大小
                self.photo_image = ImageTk.PhotoImage(photo)  # 保存引用，防止被回收
                self.left_img_label.config(image=self.photo_image)
            except Exception as e:
                print(f"Error loading image: {e}")
            # 再次显示主窗口
            self.root.deiconify()
        else:
            # 如果用户取消了操作，则直接显示窗口，不进行任何图片加载操作
            self.root.deiconify()

    def menu_register_user_info(self):
        def if_right_info():
            """ 用来测试数据是否正确 """
            pattern_username = r'^[\u4e00-\u9fa5]{3,4}$'  # 用户名：3-4个汉字字符
            pattern_phone = r'1\d{10}'  # 电话号：以数字“1”开头，后面紧跟着10个数字的字符串。
            pattern_email = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'  # 邮箱地址
            # 利用正则表达式检测数据内容
            # 检查用户名规范
            print(f"username:{username.get()}")
            print(f"username-result:{re.match(pattern_username, username.get())}")
            print(f"gender:{gender.get()}")
            print(f"phone:{phone.get()}")
            print(f"email:{email.get()}")
            if re.match(pattern_username, username.get()) is None:
                messagebox.showwarning("用户名不规范", "请输入正确的中文姓名作为用户名")
                return False
            if gender.get() != "男" and gender.get() != "女":
                messagebox.showwarning("性别输入不规范", '请输入“男”或者“女”。')
                return False
            # 检查电话号码规范
            if re.match(pattern_phone, phone.get()) is None:
                messagebox.showwarning("电话号码不规范", "请输入正确的11位电话号码")
                return False
            if re.match(pattern_email, email.get()) is None:
                messagebox.showwarning("邮箱格式不规范", "请输入正确的邮箱地址")
                return False
            messagebox.showinfo("测试通过", "测试通过，数据合法")
            return True

        def commit_info():
            if not if_right_info():
                # 没有通过测试
                messagebox.showwarning("数据不合法", "数据不合法，请重新输入！")
            # 数据合法
            # 接下来开始向数据库上传数据
            # 首先包装好用户信息
            local_gender = "M" if gender.get() == "男" else "F"
            t = (None, username.get(), local_gender, org.get(), phone.get(), email.get())  # 包装好用户信息
            u = make_user(t)
            interface = Interface()
            ret_uid = interface.insert_user(u)  # 添加用户
            print(f"test code >> GUI菜单功能添加用户返回uid：{ret_uid}")
            if ret_uid is not None:
                messagebox.showinfo("添加成功", f"新用户ID为{ret_uid}，请牢记。")
                interface.insert_record(self.admin_username, RecordType.ADD_USER, f"通过顶部菜单栏选项添加了新用户，用户id为：{ret_uid}")
            top_register_user.destroy()

        """ 接下来是保存信息的变量 """
        username = tk.StringVar()
        gender = tk.StringVar()
        org = tk.StringVar()
        phone = tk.StringVar()
        email = tk.StringVar()

        top_register_user = tk.Toplevel()
        top_register_user.title("用户信息登记")
        top_register_user.geometry("400x300+100+100")
        top_register_user.resizable(False, False)
        top_register_user.transient(self.root)
        top_register_user.grab_set()  # 禁止回到主窗体操作

        """ 接下来创建信息登记表 """
        # 创建全部标签
        info_label_style = ttk.Style()
        info_label_style.configure("userInfo.TLabel", font=("微软雅黑", 12))
        user_name_label = ttk.Label(top_register_user, text="      用户名：", style="userInfo.TLabel")
        user_gender_label = ttk.Label(top_register_user, text="        性别：", style="userInfo.TLabel")
        user_org_label = ttk.Label(top_register_user, text="  所属组织：", style="userInfo.TLabel")
        user_phone_label = ttk.Label(top_register_user, text="电话号码:", style="userInfo.TLabel")
        user_email_label = ttk.Label(top_register_user, text="  电子邮箱：", style="userInfo.TLabel")
        # 全部grid布局
        user_name_label.grid(row=0, column=0, padx=(50, 20), pady=(20, 5))
        user_gender_label.grid(row=1, column=0, padx=(50, 20), pady=5)
        user_org_label.grid(row=2, column=0, padx=(50, 20), pady=5)
        user_phone_label.grid(row=3, column=0, padx=(50, 20), pady=5)
        user_email_label.grid(row=4, column=0, padx=(50, 20), pady=5)
        # 全部输入框
        info_entry_style = ttk.Style()
        info_entry_style.configure("userInfoEntry.TEntry")
        user_name_entry = ttk.Entry(top_register_user, textvariable=username, style="userInfoEntry.TEntry")
        user_gender_entry = ttk.Entry(top_register_user, textvariable=gender, style="userInfoEntry.TEntry")
        user_org_entry = ttk.Entry(top_register_user, textvariable=org, style="userInfoEntry.TEntry")
        user_phone_entry = ttk.Entry(top_register_user, textvariable=phone, style="userInfoEntry.TEntry")
        user_email_entry = ttk.Entry(top_register_user, textvariable=email, style="userInfoEntry.TEntry")
        # 全部grid
        user_name_entry.grid(row=0, column=1, padx=(5, 5), pady=(20, 5))
        user_gender_entry.grid(row=1, column=1, padx=(5, 5), pady=5)
        user_org_entry.grid(row=2, column=1, padx=(5, 5), pady=5)
        user_phone_entry.grid(row=3, column=1, padx=(5, 5), pady=5)
        user_email_entry.grid(row=4, column=1, padx=(5, 5), pady=5)
        # 创建测试和提交按钮
        btn_style = ttk.Style()
        btn_style.configure("userRegisterBtn.TButton", font=("微软雅黑", 10), width=10, height=2)
        test_btn = ttk.Button(top_register_user, text="测试数据合法性", command=if_right_info,
                              style="userRegisterBtn.TButton")
        submit_btn = ttk.Button(top_register_user, text="提交数据", command=commit_info,
                                style="userRegisterBtn.TButton")
        test_btn.grid(row=5, column=1, padx=5, pady=5, ipady=2, ipadx=10)
        submit_btn.grid(row=6, column=1, padx=5, pady=5, ipady=2, ipadx=10)

    def menu_register_plate_info(self):
        """
        用来登记车牌信息
        :return:
        """

        def if_right_info() -> bool:
            """
            判断输入的车牌信息是否合法
            :return:
            """
            # 获取输入数据
            pnum_info = pnum.get()
            remark_info = text_plate_remark.get('1.0', tk.END)
            # 去除备注信息结尾的回车
            if remark_info[-1] == "\n":
                remark_info = remark_info[:-1]
            # 打印输入数据
            print("test code >> 车牌信息合法性检测")
            print(f"test code >> pnum:{pnum_info}; remark:{remark_info};")
            # 合法性判断
            # 判断空串
            if (pnum_info == "") or (pnum_info is None) or (remark_info == "") or (remark_info is None):
                messagebox.showwarning("不得为空", "输入信息不能为空")
                return False
            # 判断车牌号合法性
            pattern = "^[A-Z0-9]{6}$"
            if re.match(pattern, pnum_info) is None:
                messagebox.showwarning("错误车牌号", "应输入大写字母和数字，共六位字符")
                return False
            messagebox.showinfo("通过", "有效性测试通过")
            return True

        def commit_info() -> None:
            if not if_right_info():
                # 没有通过测试
                messagebox.showwarning("数据不合法", "数据不合法，请重新输入！")
            # 数据合法
            # 接下来开始向数据库上传数据
            # 首先包装好用户信息
            # 上传数据
            p = Plate.Plate(pnum.get(), text_plate_remark.get('1.0', tk.END))
            interface = Interface()
            ret_pid = interface.insert_plate(p)
            print(f"test code >> 添加车牌的返回结果ID为：{ret_pid}")
            if ret_pid is not None:
                messagebox.showinfo("车牌信息添加完成", f"车牌ID为{ret_pid}，请牢记。")
                interface.insert_record(self.admin_username, RecordType.ADD_PLATE, f"通过顶部菜单栏添加车牌信息：{ret_pid}")
            top_register_plate.destroy()

        pnum = tk.StringVar()
        remark = tk.StringVar()

        top_register_plate = tk.Toplevel()
        top_register_plate.title("牌照信息登记")
        top_register_plate.geometry("400x300+100+100")
        top_register_plate.resizable(False, False)
        top_register_plate.transient(self.root)
        top_register_plate.grab_set()  # 禁止

        # 创建组件
        virtual_label = tk.Label(top_register_plate)
        virtual_label.grid(row=0, pady=(5, 0))
        label_style = ttk.Style()
        label_style.configure("plateRegisterStyle.TLabel", font=("微软雅黑", 13))
        label_plate_num = ttk.Label(top_register_plate, text="牌照号码：", style="plateRegisterStyle.TLabel")  # 标签组件
        label_plate_remark = ttk.Label(top_register_plate, text="备注信息：", style="plateRegisterStyle.TLabel")  # 标签组件
        label_plate_num.grid(row=1, column=0, sticky="news", padx=25, pady=10)
        label_plate_remark.grid(row=2, column=0, sticky="news", padx=25, pady=5)
        entry_plate_num = ttk.Entry(top_register_plate, textvariable=pnum)
        text_plate_remark = tk.Text(top_register_plate, width=30, height=5)
        default_text = "默认信息。"  # 为文本框添加默认内容
        text_plate_remark.insert(tk.END, default_text)
        entry_plate_num.grid(row=1, column=1, sticky="news", padx=10, pady=10)
        text_plate_remark.grid(row=2, column=1, sticky="news", padx=10, pady=10)

        # 创建按钮
        btn_style = ttk.Style()
        # 注意，这里的样式是用户信息提交页面的按钮样式，直接拿过来用了。
        btn_check = ttk.Button(top_register_plate, text="检查信息有效性", style="btnStyle.TButton",
                               command=if_right_info)
        btn_submit = ttk.Button(top_register_plate, text="提交信息", style="btnStyle.TButton", command=commit_info)
        btn_check.grid(row=3, column=1, pady=10)
        btn_submit.grid(row=4, column=1)

    def menu_query_userinfo(self):
        """
        搜索用户信息界面
        :return:
        """

        # 创建搜索函数
        def query_userinfo_by_uid():
            """
            通过uid搜索用户信息
            :return:
            """
            # 首先获取用户输入
            local_uid_data = local_uid.get()
            # 然后判断输入是否合法
            if int(local_uid_data) < 10000 or int(local_uid_data) > 19999:
                messagebox.showwarning("uid不合法", "输入10000-19999的用户id进行查询")
            # 然后搜索用户信息
            interface = Interface()
            u = interface.select_userinfo(local_uid_data)
            u.print_user_info()
            interface.insert_record(self.admin_username, RecordType.CHECK_USER, f"通过顶部菜单栏搜索用户：{local_uid_data}")
            # 最后显示用户信息
            local_username.set(u.uname)
            local_gender.set("男" if u.gender == Gender.Gender.MALE else "女")
            local_org.set(u.org)
            local_phone.set(u.phone)
            local_email.set(u.email)

        """ 接下来是保存信息的变量 """
        local_uid = tk.StringVar()  # 用uid搜索用户信息
        local_username = tk.StringVar()
        local_gender = tk.StringVar()
        local_org = tk.StringVar()
        local_phone = tk.StringVar()
        local_email = tk.StringVar()
        """ 测试代码:用来测试信息展示 """
        local_username.set("这里显示用户名")
        local_gender.set("这里显示性别")
        local_org.set("所属组织")
        local_phone.set("电话号码")
        local_email.set("联系邮箱")
        """ 下面开始创建子窗口 """
        top_query_userinfo = tk.Toplevel()
        top_query_userinfo.title("用户信息搜索")
        top_query_userinfo.geometry("400x300+100+100")
        top_query_userinfo.resizable(False, False)
        top_query_userinfo.transient(self.root)
        top_query_userinfo.grab_set()  # 禁止回到主窗体操作
        """ 下面开始创建组件 """
        # 创建信息展示组件的标签部分
        query_userinfo_style = ttk.Style()
        query_userinfo_style.configure("queryUserInfoLabel.TLabel", font=("微软雅黑", 13))
        label_uname_info = ttk.Label(top_query_userinfo, text="    用户名：", style="queryUserInfoLabel.TLabel")
        label_gender_info = ttk.Label(top_query_userinfo, text="      性别：", style="queryUserInfoLabel.TLabel")
        label_org_info = ttk.Label(top_query_userinfo, text="所属组织：", style="queryUserInfoLabel.TLabel")
        label_phone_info = ttk.Label(top_query_userinfo, text="联系电话：", style="queryUserInfoLabel.TLabel")
        label_email_info = ttk.Label(top_query_userinfo, text="联系邮箱：", style="queryUserInfoLabel.TLabel")
        label_uname_info.grid(row=0, column=0, padx=(50, 5), pady=(20, 5))
        label_gender_info.grid(row=1, column=0, padx=(50, 5), pady=5)
        label_org_info.grid(row=2, column=0, padx=(50, 5), pady=5)
        label_phone_info.grid(row=3, column=0, padx=(50, 5), pady=5)
        label_email_info.grid(row=4, column=0, padx=(50, 5), pady=5)
        # 创建信息展示组件的信息部分
        query_userinfo_data_style = ttk.Style()
        query_userinfo_data_style.configure("queryUserInfoDataLabel.TLabel", font=("微软雅黑", 13),
                                            background="white", relief="groove", borderwidth=1, width=20)
        label_uname_data = ttk.Label(top_query_userinfo, textvariable=local_username,
                                     style="queryUserInfoDataLabel.TLabel")
        label_gender_data = ttk.Label(top_query_userinfo, textvariable=local_gender,
                                      style="queryUserInfoDataLabel.TLabel")
        label_org_data = ttk.Label(top_query_userinfo, textvariable=local_org, style="queryUserInfoDataLabel.TLabel")
        label_phone_data = ttk.Label(top_query_userinfo, textvariable=local_phone,
                                     style="queryUserInfoDataLabel.TLabel")
        label_email_data = ttk.Label(top_query_userinfo, textvariable=local_email,
                                     style="queryUserInfoDataLabel.TLabel")
        label_uname_data.grid(row=0, column=1, padx=5, pady=(20, 5))
        label_gender_data.grid(row=1, column=1, padx=5, pady=5)
        label_org_data.grid(row=2, column=1, padx=5, pady=5)
        label_phone_data.grid(row=3, column=1, padx=5, pady=5)
        label_email_data.grid(row=4, column=1, padx=5, pady=5)
        # 创建搜索框(搜索框放在最下面)
        label_query_info = ttk.Label(top_query_userinfo, text="          输入uid：", style="queryUserInfoLabel.TLabel")
        style_entry_query = ttk.Style()
        style_entry_query.configure("queryUserInfoDataEntry.TEntry")
        entry_query_userinfo = ttk.Entry(top_query_userinfo, textvariable=local_uid,
                                         style="queryUserInfoDataEntry.TEntry")
        label_query_info.grid(row=5, column=0, padx=5)
        entry_query_userinfo.grid(row=5, column=1, padx=5)
        # 创建按钮
        btn_query_userinfo = ttk.Button(top_query_userinfo, text="搜索", command=query_userinfo_by_uid)
        btn_query_userinfo.grid(row=6, column=1, pady=(10, 0))

    def menu_about_product(self):
        """
        显示产品信息
        :return:
        """
        # 创建子窗口
        top_about_product = tk.Toplevel()
        top_about_product.title("关于产品")
        top_about_product.geometry("400x300+100+100")
        top_about_product.resizable(False, False)
        top_about_product.transient(self.root)
        top_about_product.grab_set()  # 禁止回到主窗体操作
        # 创建组件
        win11_logo = Image.open('../product_img/win11_logo.png')
        new_width = 300
        print(f"new width = {new_width}")
        new_height = int(win11_logo.height * (new_width / win11_logo.width))
        resized_win11_logo = win11_logo.resize((new_width, new_height))
        win11_logo = ImageTk.PhotoImage(resized_win11_logo)
        label_title_logo = tk.Label(top_about_product, image=win11_logo)
        label_title_logo.image = win11_logo
        label_title_logo.pack()
        # 模拟一个分割线
        frm_dividing_line = tk.Frame(top_about_product, borderwidth=1, relief='groove', height=2)
        frm_dividing_line.pack(fill="x", padx=10, pady=10)
        # 创建描述标签
        str_info = "本产品作用于\n张浩田的“校园电动车车牌识别”毕业设计\n请勿用于无关场合。"
        label_info = tk.Label(top_about_product, text=str_info, justify='left', font=("微软雅黑", 13))
        label_info.pack(pady=(20, 0))

    def menu_query_plate(self):
        """
        检索车牌信息
        :return:
        """

        def select_plate():
            """
            搜索车牌信息的函数
            :return:
            """
            pid = local_pid.get()  # 获取要搜索的车牌信息
            print(f"test code >> 要搜索的车牌ID是：{pid}")
            # 合法性检查
            if pid == "" or pid is None:
                messagebox.showwarning("不得为空", "输入车牌号码ID不能为空")
                return None
            if int(pid) < 20000 or int(pid) > 29999:
                messagebox.showwarning("非法数据", "非法数据，请输入正确范围内的车牌号码id")
                return None
            # 通过合法性检查
            # 接下来连接数据库搜索数据
            interface = Interface()
            p = interface.select_plate_info(pid)  # 搜索pid
            interface.insert_record(self.admin_username, RecordType.CHECK_PLATE, f"通过顶部菜单栏搜索车牌信息：{pid}")
            # 然后显示数据
            local_pnum.set(p.pnum)
            local_remark.set(p.remark)
            # 设置text文本框内容
            text_show_remark.config(state=tk.NORMAL)  # 先设置为可修改状态
            text_show_remark.delete("1.0", tk.END)  # 删除原先内容
            text_show_remark.insert(tk.END, local_remark.get())  # 插入新内容
            text_show_remark.config(state=tk.DISABLED)  # 改回禁用状态

        # 创建本地变量
        local_pid = tk.StringVar()
        local_pnum = tk.StringVar()
        local_remark = tk.StringVar()
        # 创建子窗口
        top_query_plate = tk.Toplevel()
        top_query_plate.title("用户信息搜索")
        top_query_plate.geometry("400x300+100+100")
        top_query_plate.resizable(False, False)
        top_query_plate.transient(self.root)
        top_query_plate.grab_set()  # 禁止回到主窗体操作
        # 信息标注组件
        # 信息标签的样式设置
        style_mark_plate = ttk.Style()
        style_mark_plate.configure("queryPlateMarkLabelStyle.TLabel", font=("微软雅黑", 13))
        label_mark_plate = ttk.Label(top_query_plate, text="   牌照号码: ", style="queryPlateMarkLabelStyle.TLabel")
        label_mark_remark = ttk.Label(top_query_plate, text="数据库备注: ", style="queryPlateMarkLabelStyle.TLabel")
        label_mark_plate.grid(row=0, column=0, padx=(50, 5), pady=(20, 5))
        label_mark_remark.grid(row=1, column=0, padx=(50, 5), pady=5)
        # 信息显示组件
        style_show_plate = ttk.Style()  # 显示车牌号码的标签样式
        style_show_plate.configure("queryPlateShowLabelStyle.TLabel", font=("微软雅黑", 13),
                                   background="white", relief="groove", borderwidth=1, width=20)
        label_show_plate = ttk.Label(top_query_plate, textvariable=local_pnum, style="queryPlateShowLabelStyle.TLabel")
        text_show_remark = tk.Text(top_query_plate, height=5, width=28, state="disabled")
        label_show_plate.grid(row=0, column=1, padx=5, pady=(20, 5))
        text_show_remark.grid(row=1, column=1, padx=5, pady=5)
        # 创建搜索按钮
        style_query_label = ttk.Style()
        style_query_label.configure("styleQueryByPnum.TLabel", font=("微软雅黑", 13))
        label_query_by_pnum = ttk.Label(top_query_plate, text="            输入ID:", style="styleQueryByPnum.TLabel")
        entry_query_by_pnum = ttk.Entry(top_query_plate, textvariable=local_pid, width=20)
        btn_query_by_pnum = ttk.Button(top_query_plate, text="搜索", command=select_plate)
        label_query_by_pnum.grid(row=2, column=0, padx=5, pady=5)
        entry_query_by_pnum.grid(row=2, column=1, padx=5, pady=5)
        btn_query_by_pnum.grid(row=3, column=1, padx=5, pady=5)

    def menu_add_relation(self):
        """
        用于添加新关系的功能按键
        在添加关系的模型中
        :return:
        """

        def check_legal() -> bool:
            """
            判断数据是否合法
            :return:
            """
            # 判断uid
            if int(local_uid.get()) < 10000 or int(local_uid.get()) > 19999:
                messagebox.showwarning("非法数据", "uid数据不合法，请重新输入。")
                return False
            if int(local_pid.get()) < 20000 or int(local_pid.get()) > 29999:
                messagebox.showwarning("非法数据", "pid数据不合法，请重新输入。")
                return False
            messagebox.showinfo("合法数据", "数据合法，检查通过")
            return True

        def commit_info():
            """
            提交信息按钮功能
            :return:
            """
            # 先检查一次数据是否合法
            if not check_legal():
                return  # 数据非法，不作为
            # 数据合法，提交信息
            interface = Interface()
            interface.insert_relation(local_uid.get(), local_pid.get())
            messagebox.showinfo("添加成功", "绑定信息添加成功")

        # 创建本地变量
        local_uid = tk.StringVar()
        local_pid = tk.StringVar()
        # 创建子窗口
        top_add_bind = tk.Toplevel()
        top_add_bind.title("添加绑定关系")
        top_add_bind.geometry("400x300+100+100")
        top_add_bind.resizable(False, False)
        top_add_bind.transient(self.root)
        top_add_bind.grab_set()  # 禁止回到主窗体操作
        # 创建标签组件
        style_label_mark = ttk.Style()
        style_label_mark.configure("styleLabelMark.TLabel", font=("微软雅黑", 13))
        label_mark_uid = ttk.Label(top_add_bind, text="用户ID：", style="styleLabelMark.TLabel")
        label_mark_pid = ttk.Label(top_add_bind, text="车牌ID：", style="styleLabelMark.TLabel")
        label_mark_uid.grid(row=1, column=1, padx=(50, 5), pady=(20, 5))
        label_mark_pid.grid(row=2, column=1, padx=(50, 5), pady=5)
        # 创建输入组件
        style_entry = ttk.Style()
        style_entry.configure("styleEntry.TEntry", font=("微软雅黑", 13))
        entry_uid = ttk.Entry(top_add_bind, textvariable=local_uid, style="styleEntry.TEntry")
        entry_pid = ttk.Entry(top_add_bind, textvariable=local_pid, style="styleEntry.TEntry")
        entry_uid.grid(row=1, column=2, padx=10, pady=(20, 5))
        entry_pid.grid(row=2, column=2, padx=10, pady=(5, 5))
        # 创建信息检查按钮
        style_btn = ttk.Style()
        style_btn.configure("styleBtn.TButton", font=("微软雅黑", 13), width=20)
        btn_check = ttk.Button(top_add_bind, text="检查信息", command=check_legal)
        btn_check.grid(row=3, column=2, padx=20, pady=10)
        # 创建登记按钮
        btn_commit = ttk.Button(top_add_bind, text="登记信息", command=commit_info)
        btn_commit.grid(row=4, column=2)

    def menu_quick_add_relation(self):
        """
        快速添加新关系（包括添加用户、添加车牌、添加关系）
        :return:
        """

        def quick_add():
            """
            快速添加功能
            :return:
            """
            print(f"test code >> 开始执行快速添加功能")
            # 第一步：创建用户实例
            # 先准备数据
            # 改好性别
            real_gender: Gender.Gender
            if local_gender.get() == "男":
                real_gender = Gender.Gender.MALE
            else:
                real_gender = Gender.Gender.FEMALE
            # 包装用户实例
            u = User.User(local_uname.get(), real_gender, local_org.get(), local_phone.get(), local_email.get())
            # 第二步：创建车牌实例
            local_remark.set(text_mark_remark.get("1.0", tk.END))
            p = Plate.Plate(local_pnum.get(), local_remark.get())
            # 第三步：创建统一接口实例，执行快速添加功能
            interface = Interface()
            ret_info = interface.quick_add_relation(u, p)
            # 返回执行结果
            print(f"test code >> 快速添加功能添加结果为：{ret_info}")
            # 提示信息
            messagebox.showinfo("处理结果",
                                f"被添加的用户uid为：{ret_info[0]}\n被添加的车牌pid为：{ret_info[1]}"
                                f"\n被添加的关系rid 为：{ret_info[2]}\n请务必保存好您的信息！")

        # 创建本地变量
        local_uid = tk.StringVar()
        local_uname = tk.StringVar()
        local_gender = tk.StringVar()
        local_org = tk.StringVar()
        local_phone = tk.StringVar()
        local_email = tk.StringVar()

        local_pid = tk.StringVar()
        local_pnum = tk.StringVar()
        local_remark = tk.StringVar()

        local_r_remark = tk.StringVar()  # 这个是绑定关系的备注

        # 创建子窗口
        top_quick_add = tk.Toplevel()
        top_quick_add.title("快速绑定")
        top_quick_add.geometry("500x300+100+100")
        top_quick_add.resizable(False, False)
        top_quick_add.transient(self.root)
        top_quick_add.grab_set()  # 禁止回到主窗体操作

        # 用户信息部分
        # 创建说明性标签
        style_label_mark = ttk.Style()
        style_label_mark.configure("styleLabelMark.TLabel", font=("微软雅黑", 13))
        label_mark_uname = ttk.Label(top_quick_add, text="用户姓名：", style="styleLabelMark.TLabel")
        label_mark_gender = ttk.Label(top_quick_add, text="用户性别：", style="styleLabelMark.TLabel")
        label_mark_org = ttk.Label(top_quick_add, text="所属组织：", style="styleLabelMark.TLabel")
        label_mark_phone = ttk.Label(top_quick_add, text="联系电话：", style="styleLabelMark.TLabel")
        label_mark_email = ttk.Label(top_quick_add, text="联系邮箱：", style="styleLabelMark.TLabel")
        # 标签布局
        label_mark_uname.grid(row=0, column=0, padx=(20, 5), pady=(30, 5))
        label_mark_gender.grid(row=1, column=0, padx=(20, 5), pady=5)
        label_mark_org.grid(row=2, column=0, padx=(20, 5), pady=5)
        label_mark_phone.grid(row=3, column=0, padx=(20, 5), pady=5)
        label_mark_email.grid(row=4, column=0, padx=(20, 5), pady=5)
        # 创建entry组件
        entry_uname = ttk.Entry(top_quick_add, textvariable=local_uname)
        entry_gender = ttk.Entry(top_quick_add, textvariable=local_gender)
        entry_org = ttk.Entry(top_quick_add, textvariable=local_org)
        entry_phone = ttk.Entry(top_quick_add, textvariable=local_phone)
        entry_email = ttk.Entry(top_quick_add, textvariable=local_email)
        # 输入框布局
        entry_uname.grid(row=0, column=1, padx=5, pady=(32, 5))
        entry_gender.grid(row=1, column=1, padx=5, pady=5)
        entry_org.grid(row=2, column=1, padx=5, pady=5)
        entry_phone.grid(row=3, column=1, padx=5, pady=5)
        entry_email.grid(row=4, column=1, padx=5, pady=5)
        # 车牌信息部分
        label_mark_pnum = ttk.Label(top_quick_add, text="车牌号码：", style="styleLabelMark.TLabel")
        label_mark_remark = ttk.Label(top_quick_add, text="车牌备注:", style="styleLabelMark.TLabel")
        entry_pnum = ttk.Entry(top_quick_add, textvariable=local_pnum)
        text_mark_remark = tk.Text(top_quick_add, width=24, height=4)
        text_mark_remark.insert("end", "在此输入车牌信息备注")
        # 车牌信息部分组件布局
        label_mark_pnum.grid(row=0, column=2, padx=(20, 5), pady=(30, 5), sticky="w")
        entry_pnum.grid(row=1, column=2, padx=(20, 5), pady=5, sticky="w")
        label_mark_remark.grid(row=2, column=2, padx=(20, 5), pady=5, sticky="w")
        text_mark_remark.grid(row=3, column=2, rowspan=2, padx=(20, 5), pady=10, sticky="w")

        # 创建信息组备注信息
        label_mark_uni_remark = ttk.Label(top_quick_add, text="关系备注：", style="styleLabelMark.TLabel")
        text_uni_remark = tk.Text(top_quick_add, width=20, height=3)
        label_mark_uni_remark.grid(row=5, column=0, padx=(20, 5), pady=(20, 5))
        text_uni_remark.grid(row=5, column=1, padx=5, pady=10, sticky="nw")

        # 创建功能性按钮组件
        btn_check = ttk.Button(top_quick_add, text="检查信息")
        btn_commit = ttk.Button(top_quick_add, text="提交信息", command=quick_add)
        btn_check.grid(row=5, column=2, sticky="w", padx=(20, 3))
        btn_commit.grid(row=5, column=2, sticky="e", padx=(5, 0))

    def create_menubar(self):
        """ 创建顶部菜单栏的函数
        """
        """ 创建顶部菜单栏 """
        total_menubar = tk.Menu(self.root)
        self.root.config(menu=total_menubar)
        """ 创建“文件”菜单 """
        file_menu = tk.Menu(total_menubar, tearoff=0)  # 创建“文件”菜单
        total_menubar.add_cascade(label="文件", menu=file_menu)  # 在总菜单中添加级联菜单
        file_menu.add_command(label="导入图片", command=self.menu_import_file)  # 在级联菜单中添加子按钮
        """ 创建“登记”菜单 """
        register_menu = tk.Menu(total_menubar, tearoff=0)
        total_menubar.add_cascade(label="登记", menu=register_menu)
        register_menu.add_command(label="登记用户信息", command=self.menu_register_user_info)
        register_menu.add_command(label="登记车牌信息", command=self.menu_register_plate_info)
        """ 创建“检索”菜单 """
        register_menu = tk.Menu(total_menubar, tearoff=0)
        total_menubar.add_cascade(label="检索", menu=register_menu)
        register_menu.add_command(label="检索用户信息", command=self.menu_query_userinfo)
        register_menu.add_command(label="检索车牌信息", command=self.menu_query_plate)
        # register_menu.add_command(label="检索人车关系")
        """ 创建“修改”菜单 
        register_menu = tk.Menu(total_menubar, tearoff=0)
        total_menubar.add_cascade(label="修改", menu=register_menu)
        register_menu.add_command(label="修改用户信息")
        register_menu.add_command(label="修改车牌信息")
        """
        # register_menu.add_command(label="修改人车关系")
        """ 创建“删除”菜单 
        register_menu = tk.Menu(total_menubar, tearoff=0)
        total_menubar.add_cascade(label="删除", menu=register_menu)
        register_menu.add_command(label="删除用户信息")
        register_menu.add_command(label="删除车牌信息")
        register_menu.add_command(label="删除人车关系")
        """
        """ 创建“绑定”菜单 """
        register_menu = tk.Menu(total_menubar, tearoff=0)
        total_menubar.add_cascade(label="绑定", menu=register_menu)
        register_menu.add_command(label="绑定人车关系", command=self.menu_add_relation)
        register_menu.add_command(label="快速添加", command=self.menu_quick_add_relation)
        """ 创建“绑定”菜单 """
        register_menu = tk.Menu(total_menubar, tearoff=0)
        total_menubar.add_command(label="关于(产品)", command=self.menu_about_product)

    def fun_identify(self):
        """
        用来调用统一接口的一键识别函数
        :return:
        """
        # 创建接口层实例
        interface = Interface()
        # 调用识别模块
        identify_ret = interface.interface_identify(self.file_path)  # 调用统一接口执行车牌识别，并且获得返回值
        print(f"车牌区域图片的绝对地址为：{identify_ret}")
        # 获得了识别结果后，下一步就是将识别结果的图片和字符串打印到界面中
        plate_area_path = identify_ret[0]  # 图片地址
        plate_number = identify_ret[1]  # 识别结果
        # 设置显示图片
        right_show_image = Image.open(plate_area_path)
        right_shown_img = ImageTk.PhotoImage(right_show_image.resize((300, 150)))
        self.right_img_label.config(image=right_shown_img)
        self.right_img_label.image = right_shown_img
        # 设置显示字符
        self.var_plate_number.set(plate_number)
        # 保留搜索记录
        interface.insert_record(self.admin_username, RecordType.IDENTIFY, f"搜索车牌信息,车牌号码：{plate_number}")

    def fun_copy_label(self, event):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.var_plate_number.get())

    def fun_select_master(self):
        """
        这个函数用来设计查找车主的功能
        :return:
        """
        # 创建统一结构
        interface = Interface()
        master_info = None
        try:
            master_info = interface.interface_select_master_by_plate(self.var_plate_number.get())
        except Exception as e:
            print(f"错误信息：{e}")
            messagebox.showwarning("搜索失败", "用户信息搜索失败")
            return
        print(f"查询到的车主信息: {master_info}")

        # 现在的master_info是一个User类型的对象
        # 接下来创建Topleve窗口显示User信息
        top_master_info = tk.Toplevel()
        top_master_info.title("查询结果")
        top_master_info.geometry("400x300+100+100")
        top_master_info.resizable(False, False)
        top_master_info.transient(self.root)
        top_master_info.grab_set()  # 禁止回到主窗体操作
        # 设置具体内容
        # 创建题目标签
        style_title = ttk.Style()
        style_title.configure("topMasterTitle.TLabel", font=("微软雅黑", 16))
        label_title = ttk.Label(top_master_info, text="搜索结果", style="topMasterTitle.TLabel")
        label_title.grid(row=0, column=0, columnspan=2, pady=(10, 0), padx=100)
        # 创建标签列表
        style_top_master = ttk.Style()
        style_top_master.configure("topMasterShowStyle.TLabel", font=("微软雅黑", 13))
        label_uname = ttk.Label(top_master_info, text="    用户名：", style="topMasterShowStyle.TLabel")
        label_gender = ttk.Label(top_master_info, text="      性别：", style="topMasterShowStyle.TLabel")
        label_org = ttk.Label(top_master_info, text="所属组织：", style="topMasterShowStyle.TLabel")
        label_phone = ttk.Label(top_master_info, text="联系电话：", style="topMasterShowStyle.TLabel")
        label_email = ttk.Label(top_master_info, text="联系邮箱：", style="topMasterShowStyle.TLabel")
        label_plate = ttk.Label(top_master_info, text="车牌号码：", style="topMasterShowStyle.TLabel")
        label_uname.grid(row=1, column=0, padx=(20, 5), pady=(10, 5))
        label_gender.grid(row=2, column=0, padx=(20, 5), pady=5)
        label_org.grid(row=3, column=0, padx=(20, 5), pady=5)
        label_phone.grid(row=4, column=0, padx=(20, 5), pady=5)
        label_email.grid(row=5, column=0, padx=(20, 5), pady=5)
        label_plate.grid(row=6, column=0, padx=(20, 5), pady=5)
        # 创建展示标签
        style_top_master = ttk.Style()
        style_top_master.configure("topMasterContentStyle.TLabel", font=("微软雅黑", 13),
                                   relief="sunken", borderwidth=1, background="white", width=25)
        label_uname_info = ttk.Label(top_master_info, text=master_info.uname, style="topMasterContentStyle.TLabel")
        label_gender = ttk.Label(top_master_info, text=master_info.gender, style="topMasterContentStyle.TLabel")
        label_org = ttk.Label(top_master_info, text=master_info.org, style="topMasterContentStyle.TLabel")
        label_phone = ttk.Label(top_master_info, text=master_info.phone, style="topMasterContentStyle.TLabel")
        label_email = ttk.Label(top_master_info, text=master_info.email, style="topMasterContentStyle.TLabel")
        label_plate = ttk.Label(top_master_info, textvariable=self.var_plate_number,
                                style="topMasterContentStyle.TLabel")
        label_uname_info.grid(row=1, column=1, padx=5, pady=(20, 5))
        label_gender.grid(row=2, column=1, padx=5, pady=5)
        label_org.grid(row=3, column=1, padx=5, pady=5)
        label_phone.grid(row=4, column=1, padx=5, pady=5)
        label_email.grid(row=5, column=1, padx=5, pady=5)
        label_plate.grid(row=6, column=1, padx=5, pady=5)
        # print(f">> 车牌号码：{self.var_plate_number.get()}")
        interface.insert_record(self.admin_username, RecordType.CHECK_USER,
                                f"通过车牌号码{self.var_plate_number.get()}查询车主{master_info.uname}")

    def fun_register_plate(self):
        """
        该函数用于登记车牌信息
        :return:
        """

        def sub_fun_commit_register():
            # 提交车牌信息（主要是备注）
            remark_text = text_remark_data.get("1.0", tk.END)
            print(f"test-code >> 车牌备注信息是：{remark_text}")
            interface = Interface()
            ret_pid = None
            try:
                ret_pid = interface.insert_insert_plate(self.var_plate_number.get(), remark_text)
            except Exception as e:
                print(f"添加车牌信息出现错误:{e}")
                messagebox.showwarning("添加出错", "添加车牌出错，车牌已存在。")
            if ret_pid is not None:
                messagebox.showinfo("车牌信息添加完成", f"车牌ID为{ret_pid}，请牢记。")
            top_register_plate.destroy()

        # 创建子窗口
        top_register_plate = tk.Toplevel()
        top_register_plate.title("用户信息搜索")
        top_register_plate.geometry("400x300+100+100")
        top_register_plate.resizable(False, False)
        top_register_plate.transient(self.root)
        top_register_plate.grab_set()  # 禁止回到主窗体操作
        # 创建标题组件
        style_label_title = ttk.Style()
        style_label_title.configure("styleTitle.TLabel", font=("微软雅黑", 16))
        label_title = ttk.Label(top_register_plate, text="登记车牌", style="styleTitle.TLabel")
        label_title.grid(row=0, column=0, columnspan=2, pady=(10, 0), padx=(60, 5))
        # 创建标签组件
        style_top_master = ttk.Style()
        style_top_master.configure("styleRegisterShowLabel.TLabel", font=("微软雅黑", 13))
        label_pnum = ttk.Label(top_register_plate, text="车牌号码：", style="styleRegisterShowLabel.TLabel")
        label_remark = ttk.Label(top_register_plate, text="车牌备注：", style="styleRegisterShowLabel.TLabel")
        label_pnum.grid(row=1, column=0, padx=(50, 10), pady=(10, 5))
        label_remark.grid(row=2, column=0, padx=(50, 10), pady=5)
        # 创建展示组件
        style_shown_label = ttk.Style()
        style_shown_label.configure("styleRegisterShownLabel.TLabel", font=("微软雅黑", 13),
                                    relief="sunken", borderwidth=1, background="white", width=15)
        label_pnum_data = ttk.Label(top_register_plate, textvariable=self.var_plate_number,
                                    style="styleRegisterShownLabel.TLabel")
        text_remark_data = tk.Text(top_register_plate, width=22, height=5, font=("微软雅黑", 10))
        default_text = "默认。"  # 为文本框添加默认内容
        text_remark_data.insert(tk.END, default_text)
        label_pnum_data.grid(row=1, column=1, padx=5, pady=5)
        text_remark_data.grid(row=2, column=1, padx=5, pady=5)
        # 创建提交按钮
        style_btn = ttk.Style()
        style_btn.configure("styleRegisterBtn.TButton", font=("微软雅黑", 13), width=10, height=2)
        btn_register = ttk.Button(top_register_plate, text="提交信息", style="styleRegisterBtn.TButton",
                                  command=sub_fun_commit_register)
        btn_register.grid(row=3, column=1, padx=5, pady=5)

    def create_gui(self):
        """ 创建全部gui组件 """
        """ 创建菜单组件 """
        self.create_menubar()  # 调用函数创建顶部菜单栏
        """ 创建其他组件 """
        # 创建左右框架
        side_frm_style = ttk.Style()
        # side_frm_style.configure("sideFrame.TFrame", width="50%", height="100%",
        #                          borderwidth=1, relief="groove")
        side_frm_style.configure("sideFrame.TFrame", width="50%", height="100%")
        self.left_frm = ttk.Frame(self.root, style="sideFrame.TFrame")
        self.right_frm = ttk.Frame(self.root, style="sideFrame.TFrame")
        self.left_frm.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        ttk.Separator(self.root, orient="vertical").pack(fill="y", side=tk.LEFT)
        self.right_frm.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 创建左右标题标签
        title_label_style = ttk.Style()
        title_label_style.configure("titleLabel.TLabel", font=("微软雅黑", 18))
        self.left_title_label = ttk.Label(self.left_frm, text="原始图片", style="titleLabel.TLabel")
        self.right_title_label = ttk.Label(self.right_frm, text="识别结果", style="titleLabel.TLabel")
        self.left_title_label.pack(side=tk.TOP, pady=(30, 10))
        self.right_title_label.pack(side=tk.TOP, pady=(30, 10))
        # 创建左右图片显示标签
        left_shown_img = Image.open("../product_img/app_logo.jpg")  # 加载图片
        left_shown_img = ImageTk.PhotoImage(left_shown_img.resize((300, 300)))
        left_img_style = ttk.Style()
        left_img_style.configure("leftImgLabel.TLabel", width="350", height="350",
                                 borderwidth=1, relief="groove")
        self.left_img_label = ttk.Label(self.left_frm, image=left_shown_img, style="leftImgLabel.TLabel")
        self.left_img_label.image = left_shown_img
        self.left_img_label.pack(pady=(10, 0))
        # 创建右侧图片
        right_shown_img = Image.open("../product_img/app_logo.jpg")
        right_shown_img = ImageTk.PhotoImage(right_shown_img.resize((300, 150)))
        right_img_style = ttk.Style()
        right_img_style.configure("rightImgLabel.TLabel", width="300", height="150",
                                  borderwidth=1, relief="groove")
        self.right_img_label = ttk.Label(self.right_frm, image=right_shown_img, style="rightImgLabel.TLabel")
        self.right_img_label.image = right_shown_img
        self.right_img_label.pack(pady=(10, 0))
        # 创建右侧复制字符提示内容
        self.right_remind_label = tk.Label(self.right_frm, text="双击复制牌照号码", font=("微软雅黑", 12, 'italic'))
        self.right_remind_label.pack(pady=(30, 0))
        # 创建右侧车牌号码显示框(Label模拟)
        self.var_plate_number.set("abcdefg")
        self.right_plate_label = tk.Label(self.right_frm, textvariable=self.var_plate_number,
                                          font=("Consolas", 14), background="white", relief="groove",
                                          width=20, height=2)
        self.right_plate_label.pack(pady=(20, 0))
        self.right_plate_label.bind("<Double-Button-1>", self.fun_copy_label)
        # 创建左侧按钮样式
        btn_style = ttk.Style()
        btn_style.configure("btnStyle.TButton", font=("微软雅黑", 12), width=13)
        # 创建左侧"一键识别"按钮
        self.left_match_btn = ttk.Button(self.left_frm, text="一键识别", style="btnStyle.TButton",
                                         command=self.fun_identify)
        self.left_match_btn.pack(pady=(0, 0), side=tk.LEFT, padx=(75, 0))
        # 创建左侧"详细信息"按钮
        self.left_details_btn = ttk.Button(self.left_frm, text="更换图片", style="btnStyle.TButton",
                                           command=self.menu_import_file)
        self.left_details_btn.pack(pady=(0, 0), side=tk.LEFT, padx=(25, 0))
        # 创建右侧"查找车主"按钮
        self.right_query_btn = ttk.Button(self.right_frm, text="查找车主", style="btnStyle.TButton",
                                          command=self.fun_select_master)
        self.right_query_btn.pack(side=tk.LEFT, padx=(70, 0), pady=(50, 27))
        # 创建右侧"登记车牌"按钮
        self.right_register_btn = ttk.Button(self.right_frm, text="登记车牌", style="btnStyle.TButton",
                                             command=self.fun_register_plate)
        self.right_register_btn.pack(side=tk.LEFT, padx=(25, 0), pady=(50, 27))
